"""
pages/3_Bulk_Analysis.py
========================
Module 8 – Bulk CSV Sentiment Analysis

Upload a CSV file and analyze all reviews at once.
Download the processed results with predicted sentiments and probabilities.
"""

import io
import os
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import SENTIMENT_COLORS
from src.database import insert_batch_predictions, init_db
from src.prediction import predict_batch, get_pipeline
from src.visualization import plot_sentiment_donut, plot_sentiment_bar
from src.icons import lucide

init_db()

@st.cache_resource(show_spinner="Loading model...")
def load_pipeline():
    return get_pipeline()

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<h1 style="color:#ffffff; font-size:2rem; font-weight:700; letter-spacing:-0.02em; margin-bottom:0.25rem; display:flex; align-items:center; gap:10px;">
    {lucide('upload', 26, '#818cf8')}
    <span>Bulk CSV Sentiment Analysis</span>
</h1>
<p style="color:#94a3b8; font-size:1rem; margin-top:0;">Upload a CSV file with reviews or comments and get sentiment predictions for all rows.</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Upload Section ────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"],
    help="The CSV must contain at least one column with text data.",
)

if uploaded_file:
    try:
        df_upload = pd.read_csv(uploaded_file)
        st.success(f"File loaded: **{uploaded_file.name}** — {len(df_upload):,} rows × {len(df_upload.columns)} columns")

        st.subheader("Preview (first 5 rows)")
        st.dataframe(df_upload.head(), use_container_width=True)

        # Column selector
        st.markdown("---")
        col_sel, col_lbl = st.columns([1, 1])

        with col_sel:
            text_col = st.selectbox(
                "Select the text column:",
                options=df_upload.columns.tolist(),
                help="The column containing the reviews or comments.",
            )
        with col_lbl:
            available_cols = ["None (no ground truth)"] + df_upload.columns.tolist()
            label_col = st.selectbox(
                "Ground-truth label column (optional):",
                options=available_cols,
                help="If available, accuracy metrics will be computed.",
            )
            has_labels = label_col != "None (no ground truth)"

        analyze_btn = st.button("Run Bulk Analysis", use_container_width=False)

        if analyze_btn:
            try:
                pipeline = load_pipeline()

                with st.spinner(f"Analyzing {len(df_upload):,} records..."):
                    result_df = predict_batch(df_upload, text_col=text_col, pipeline=pipeline)

                st.session_state["bulk_result"] = result_df
                st.session_state["bulk_label_col"] = label_col if has_labels else None

                st.success(f"Analysis complete — {len(result_df):,} records processed.")

            except FileNotFoundError:
                st.error("Model not found. Run `python train_model.py` first.")
            except Exception as e:
                st.error(f"Error during analysis: {e}")

    except Exception as e:
        st.error(f"Failed to read CSV: {e}")

# ── Results Section ───────────────────────────────────────────────────────────
if "bulk_result" in st.session_state and st.session_state["bulk_result"] is not None:
    result_df = st.session_state["bulk_result"]
    label_col = st.session_state.get("bulk_label_col")

    st.markdown("---")
    st.subheader("Results Summary")

    # KPI Metrics
    dist = result_df["predicted_sentiment"].value_counts()
    total = len(result_df)
    m_cols = st.columns(4)
    m_cols[0].metric("Total Records", f"{total:,}")
    for i, sentiment in enumerate(["Positive", "Negative", "Neutral"]):
        count = int(dist.get(sentiment, 0))
        m_cols[i + 1].metric(
            f"{sentiment}",
            f"{count:,}",
            f"{count/total*100:.1f}%",
        )

    # Charts
    c1, c2 = st.columns(2)
    with c1:
        fig_donut = plot_sentiment_donut(dist.to_dict(), "Predicted Sentiment Distribution")
        st.plotly_chart(fig_donut, use_container_width=True)
    with c2:
        fig_bar = plot_sentiment_bar(dist.to_dict(), "Sentiment Count")
        st.plotly_chart(fig_bar, use_container_width=True)

    # Optional: Ground-truth evaluation
    if label_col and label_col in result_df.columns:
        st.markdown("---")
        st.subheader("Ground-Truth Evaluation")
        from src.evaluation import compute_metrics
        from src.config import SENTIMENT_CLASSES
        try:
            metrics = compute_metrics(
                result_df[label_col],
                result_df["predicted_sentiment"],
                labels=SENTIMENT_CLASSES,
            )
            em1, em2, em3, em4 = st.columns(4)
            em1.metric("Accuracy",       f"{metrics['accuracy']:.2%}")
            em2.metric("F1 Macro",       f"{metrics['f1_macro']:.2%}")
            em3.metric("F1 Weighted",    f"{metrics['f1_weighted']:.2%}")
            em4.metric("Precision Macro",f"{metrics['precision_macro']:.2%}")
        except Exception as e:
            st.warning(f"Could not compute metrics: {e}")

    # ── Filter & Preview ──────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Preview & Filter")

    filter_sent = st.multiselect(
        "Filter by Sentiment:",
        options=["Positive", "Negative", "Neutral"],
        default=["Positive", "Negative", "Neutral"],
    )
    filtered_df = result_df[result_df["predicted_sentiment"].isin(filter_sent)]
    st.dataframe(filtered_df.head(50), use_container_width=True)
    st.caption(f"Showing {min(50, len(filtered_df))} of {len(filtered_df):,} filtered records.")

    # ── Download ──────────────────────────────────────────────────────────
    st.markdown("---")
    col_dl1, col_dl2 = st.columns(2)

    with col_dl1:
        csv_buffer = io.StringIO()
        result_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label     = "Download Full Results (CSV)",
            data      = csv_buffer.getvalue(),
            file_name = "sentiment_predictions.csv",
            mime      = "text/csv",
            use_container_width=True,
        )

    with col_dl2:
        if st.button("Save All to Database", use_container_width=True):
            try:
                prob_cols = {
                    "Positive": "prob_Positive",
                    "Negative": "prob_Negative",
                    "Neutral":  "prob_Neutral",
                }
                records = []
                for _, row in result_df.iterrows():
                    records.append({
                        "raw_text":            str(row.get(text_col, "")),
                        "clean_text":          str(row.get("clean_text", "")),
                        "predicted_sentiment": str(row["predicted_sentiment"]),
                        "prob_positive":       float(row.get("prob_Positive", 0)),
                        "prob_negative":       float(row.get("prob_Negative", 0)),
                        "prob_neutral":        float(row.get("prob_Neutral",  0)),
                        "confidence":          float(row.get("confidence", 0)),
                        "source":              "bulk_upload",
                    })
                insert_batch_predictions(records)
                st.success(f"Saved {len(records):,} predictions to the database.")
            except Exception as e:
                st.error(f"Error saving to database: {e}")

else:
    if not uploaded_file:
        st.markdown(f"""
        <div style="text-align:center;padding:3rem;color:#94a3b8;
                    border:1px dashed rgba(99,102,241,.3);border-radius:14px;margin-top:1rem;">
            <div style="margin-bottom:0.75rem;">{lucide('upload', 38, '#818cf8')}</div>
            <div style="margin-top:.5rem;font-size:1.1rem;font-weight:600;color:#f8fafc;">
                Upload a CSV file to get started
            </div>
            <div style="font-size:.85rem;margin-top:.5rem;">
                Supported format: .csv with a text column containing reviews or comments
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Instructions ──────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("CSV Format Requirements"):
    st.markdown("""
    **Required:**
    - At least one column containing text data (reviews, comments, posts)

    **Optional:**
    - A sentiment label column (for accuracy evaluation)

    **Example CSV structure:**
    ```
    text,sentiment
    "I love this product!",Positive
    "Terrible experience.",Negative
    "It was okay.",Neutral
    ```

    **Output columns added by the system:**
    - `clean_text` — preprocessed version of the text
    - `predicted_sentiment` — Positive / Negative / Neutral
    - `prob_Positive`, `prob_Negative`, `prob_Neutral` — probability scores
    - `confidence` — maximum probability (most likely class confidence)
    """)
