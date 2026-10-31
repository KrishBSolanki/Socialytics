"""
pages/7_Prediction_History.py
==============================
Module 11 – Database & Prediction History

View, filter, export, and delete prediction history stored in SQLite.
Demonstrates OLTP (record insertion) and OLAP (aggregate queries).
"""

import io
import os
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import SENTIMENT_COLORS
from src.database import (
    init_db, fetch_all_predictions, fetch_recent_predictions,
    get_prediction_stats, delete_all_predictions, delete_prediction_by_id,
    export_to_csv,
)
from src.visualization import plot_sentiment_donut, plot_sentiment_bar
from src.icons import lucide

init_db()

st.markdown(f"""
<h1 style="color:#ffffff; font-size:2rem; font-weight:700; letter-spacing:-0.02em; margin-bottom:0.25rem; display:flex; align-items:center; gap:10px;">
    {lucide('history', 26, '#818cf8')}
    <span>Prediction History</span>
</h1>
<p style="color:#94a3b8; font-size:1rem; margin-top:0;">View and manage all predictions stored in the SQLite database.</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Load Data ─────────────────────────────────────────────────────────────────
stats = get_prediction_stats()
total = stats.get("total", 0)

# ── KPI ───────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Predictions", f"{total:,}")
k2.metric("Positive",          f"{stats.get('positive', 0):,}")
k3.metric("Negative",          f"{stats.get('negative', 0):,}")
k4.metric("Neutral",           f"{stats.get('neutral', 0):,}")
k5.metric("Avg Confidence",    f"{stats.get('avg_confidence', 0):.1%}")

st.markdown("---")

if total == 0:
    st.info("""
    No predictions stored yet.

    Use the **Sentiment Analyzer** page to analyze text and save results,
    or use **Bulk Analysis** to process a CSV file.
    """)
else:
    # ── Charts ────────────────────────────────────────────────────────────
    all_df = fetch_all_predictions()

    c1, c2 = st.columns(2)
    with c1:
        dist = all_df["predicted_sentiment"].value_counts().to_dict()
        fig_d = plot_sentiment_donut(dist, "Stored Prediction Distribution")
        st.plotly_chart(fig_d, use_container_width=True)
    with c2:
        fig_b = plot_sentiment_bar(dist, "Stored Prediction Count")
        st.plotly_chart(fig_b, use_container_width=True)

    # ── Filter & Browse ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"""
    <h3 style="color:#ffffff; font-size:1.25rem; font-weight:700; margin-bottom:1rem; display:flex; align-items:center; gap:8px;">
        {lucide('search', 20, '#818cf8')}
        <span>Browse Predictions</span>
    </h3>
    """, unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        sent_filter = st.multiselect(
            "Filter by Sentiment:",
            options=["Positive", "Negative", "Neutral"],
            default=["Positive", "Negative", "Neutral"],
        )
    with fc2:
        src_options = ["All"] + all_df["source"].unique().tolist()
        src_filter  = st.selectbox("Filter by Source:", src_options)
    with fc3:
        n_rows = st.slider("Show rows:", 10, min(200, total), min(50, total))

    filtered = all_df[all_df["predicted_sentiment"].isin(sent_filter)]
    if src_filter != "All":
        filtered = filtered[filtered["source"] == src_filter]
    filtered = filtered.head(n_rows)

    # Display columns
    display_cols = [
        "id", "raw_text", "predicted_sentiment",
        "prob_positive", "prob_negative", "prob_neutral",
        "confidence", "source", "created_at",
    ]
    display_cols = [c for c in display_cols if c in filtered.columns]

    st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(filtered):,} of {total:,} total predictions.")

    # ── Export ────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"""
    <h3 style="color:#ffffff; font-size:1.25rem; font-weight:700; margin-bottom:1rem; display:flex; align-items:center; gap:8px;">
        {lucide('download', 20, '#818cf8')}
        <span>Export &amp; Manage</span>
    </h3>
    """, unsafe_allow_html=True)

    exp1, exp2, exp3 = st.columns(3)

    with exp1:
        csv_buf = io.StringIO()
        all_df.to_csv(csv_buf, index=False)
        st.download_button(
            label     = "Export as CSV",
            data      = csv_buf.getvalue(),
            file_name = "prediction_history.csv",
            mime      = "text/csv",
            use_container_width=True,
        )

    with exp2:
        json_data = all_df.to_json(orient="records", date_format="iso", indent=2)
        st.download_button(
            label     = "Export as JSON",
            data      = json_data,
            file_name = "prediction_history.json",
            mime      = "application/json",
            use_container_width=True,
        )

    with exp3:
        if "confirm_delete" not in st.session_state:
            st.session_state.confirm_delete = False

        if st.button("Clear All History", use_container_width=True):
            st.session_state.confirm_delete = True

        if st.session_state.confirm_delete:
            st.warning("This will permanently delete ALL prediction history!")
            cc1, cc2 = st.columns(2)
            with cc1:
                if st.button("Confirm Delete", use_container_width=True):
                    deleted = delete_all_predictions()
                    st.success(f"Deleted {deleted:,} records.")
                    st.session_state.confirm_delete = False
                    st.rerun()
            with cc2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.confirm_delete = False
                    st.rerun()

# ── Data Engineering Theory ───────────────────────────────────────────────────
st.markdown("---")
with st.expander("Data Engineering & OLTP vs OLAP Architecture"):
    st.markdown("""
    ### Data Pipeline in This Application

    ```
    Data Collection  ->  Data Cleaning  ->  Feature Extraction
         |                    |                     |
    Raw CSV/Text     ->  Preprocessing  ->      TF-IDF Matrix
                                                    |
    Storage (SQLite) <-  Prediction     <-  Naive Bayes Model
         |
    Visualization (Dashboard, Charts)
    ```

    ---

    ### OLTP vs OLAP

    | Feature | OLTP (this app) | OLAP (dashboard) |
    |---------|-----------------|------------------|
    | **Purpose** | Record predictions | Analyse trends |
    | **Operations** | INSERT, SELECT one record | GROUP BY, aggregate |
    | **Data Volume** | Small per query | Large scans |
    | **Example** | `INSERT INTO predictions ...` | `SELECT sentiment, COUNT(*) GROUP BY sentiment` |
    | **Response Time** | Milliseconds | Seconds |

    ### ETL Process Used Here
    - **Extract**: Load raw text from user input or CSV
    - **Transform**: Preprocess -> TF-IDF -> Predict
    - **Load**: Insert result into SQLite database
    """)
