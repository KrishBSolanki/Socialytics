"""
pages/2_Sentiment_Analyzer.py
==============================
Module 7 – Interactive Real-Time Sentiment Analyzer

Users enter a review, see predicted sentiment, probability scores,
and can save the result to the SQLite database.
"""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import SENTIMENT_COLORS
from src.database import init_db, insert_prediction
from src.prediction import predict_single, get_pipeline
from src.visualization import plot_probability_bar
from src.icons import lucide

init_db()

# ── Load model once ───────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading model...")
def load_pipeline():
    return get_pipeline()

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<h1 style="color:#ffffff; font-size:2rem; font-weight:700; letter-spacing:-0.02em; margin-bottom:0.25rem; display:flex; align-items:center; gap:10px;">
    {lucide('message-square', 26, '#818cf8')}
    <span>Interactive Sentiment Analyzer</span>
</h1>
<p style="color:#94a3b8; font-size:1rem; margin-top:0;">Enter any review, comment, or social media post to analyze its sentiment.</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Example Inputs ────────────────────────────────────────────────────────────
EXAMPLES = {
    "Positive":   "I absolutely love this product! It works perfectly and exceeded all my expectations. Highly recommend it to everyone!",
    "Negative":   "This product is terrible. It broke after just two days and customer service was completely useless. Total waste of money!",
    "Neutral":    "The product is okay. It does what it is supposed to do but nothing particularly stands out. Average experience overall.",
    "Social (+)": "Can't believe how amazing this new feature is! It's changed my workflow completely. So glad they added this!",
    "Social (-)": "Yet another broken update. Nothing works anymore. Why do they keep ruining things? Absolute disaster!",
}

# ── Two-column layout ─────────────────────────────────────────────────────────
left, right = st.columns([1.1, 1], gap="large")

with left:
    st.subheader("Enter Text")

    if "input_text" not in st.session_state:
        st.session_state["input_text"] = ""

    def set_example_text(sample_text):
        st.session_state["input_text"] = sample_text

    # Quick example buttons
    st.markdown("**Quick Examples:**")
    ex_cols = st.columns(len(EXAMPLES), gap="small")
    for i, (label, text) in enumerate(EXAMPLES.items()):
        with ex_cols[i]:
            st.button(
                label,
                key=f"ex_btn_{i}",
                use_container_width=True,
                on_click=set_example_text,
                args=(text,),
            )

    user_text = st.text_area(
        "Type or paste your review here:",
        height    = 160,
        max_chars = 5000,
        placeholder="e.g. I love this product! Great quality and fast delivery.",
        key       = "input_text",
    )

    char_count = len(user_text)
    st.caption(f"{char_count}/5000 characters")

    col_btn, col_save = st.columns([1, 1])
    with col_btn:
        analyze_clicked = st.button("Analyze Sentiment", use_container_width=True)
    with col_save:
        save_clicked    = st.button("Save to History",   use_container_width=True)

with right:
    st.subheader("Analysis Result")

    result_placeholder = st.empty()

    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    # ── Run Analysis ──────────────────────────────────────────────────────
    if analyze_clicked:
        if not user_text.strip():
            result_placeholder.error("Please enter some text before analyzing.")
        else:
            try:
                with st.spinner("Analyzing sentiment..."):
                    pipeline = load_pipeline()
                    result   = predict_single(user_text, pipeline=pipeline)
                    st.session_state.last_result = result
            except FileNotFoundError:
                st.error(
                    "Model not found. Please run the training script first:\n"
                    "```bash\npython train_model.py\n```"
                )
            except ValueError as e:
                st.error(f"Input error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

    # ── Display Result ────────────────────────────────────────────────────
    result = st.session_state.last_result
    if result:
        sentiment = result["sentiment"]
        probs     = result["probabilities"]
        conf      = result["confidence"]
        warning   = result["warning"]

        badge_class = f"badge-{sentiment.lower()}"
        color       = SENTIMENT_COLORS.get(sentiment, "#888")

        with result_placeholder.container():
            # Sentiment badge
            st.markdown(f"""
            <div style="text-align:center;padding:1.2rem;
                        background:linear-gradient(135deg,#1e1e3f,#16213e);
                        border-radius:14px;border:1px solid {color}40;margin-bottom:1rem;">
                <div style="font-size:0.8rem;color:#94a3b8;text-transform:uppercase;
                            letter-spacing:.1em;margin-bottom:.4rem;">Predicted Sentiment</div>
                <div style="font-size:2rem;font-weight:800;color:{color};">{sentiment}</div>
                <div style="font-size:0.85rem;color:#94a3b8;margin-top:.3rem;">
                    Confidence: {conf:.1%}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Probability chart
            fig = plot_probability_bar(probs, title="Probability Scores")
            st.plotly_chart(fig, use_container_width=True)

            # Probability breakdown metrics
            m1, m2, m3 = st.columns(3)
            for col_widget, cls in zip([m1, m2, m3], ["Positive", "Negative", "Neutral"]):
                with col_widget:
                    val = probs.get(cls, 0.0)
                    c   = SENTIMENT_COLORS[cls]
                    st.markdown(f"""
                    <div style="text-align:center;padding:.6rem;
                                background:{c}15;border-radius:10px;border:1px solid {c}40;">
                        <div style="font-size:.75rem;color:#94a3b8;">{cls}</div>
                        <div style="font-size:1.3rem;font-weight:700;color:{c};">{val:.1%}</div>
                    </div>
                    """, unsafe_allow_html=True)

            if warning:
                st.warning(f"Warning: {warning}")

            # Preprocessed text expander
            with st.expander("View Preprocessed Text"):
                st.code(result["clean_text"], language="text")
                st.caption("This is the text after applying the NLP preprocessing pipeline.")

        # ── Save to DB ────────────────────────────────────────────────────
        if save_clicked and result:
            try:
                row_id = insert_prediction(
                    raw_text            = result["raw_text"],
                    clean_text          = result["clean_text"],
                    predicted_sentiment = result["sentiment"],
                    prob_positive       = result["probabilities"].get("Positive", 0),
                    prob_negative       = result["probabilities"].get("Negative", 0),
                    prob_neutral        = result["probabilities"].get("Neutral",  0),
                    confidence          = result["confidence"],
                    source              = "manual",
                )
                st.success(f"Prediction saved to history (ID: {row_id})")
            except Exception as e:
                st.error(f"Failed to save: {e}")
    else:
        result_placeholder.markdown(f"""
        <div style="text-align:center;padding:3rem;color:#94a3b8;
                    border:1px dashed rgba(99,102,241,.3);border-radius:14px;">
            <div style="margin-bottom:0.75rem;">{lucide('message-square', 38, '#818cf8')}</div>
            <div>Enter text and click <b>Analyze Sentiment</b></div>
        </div>
        """, unsafe_allow_html=True)

# ── Theory expander ───────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("How Does This Work? (Pipeline Architecture)"):
    st.markdown("""
    ### Prediction Pipeline

    1. **Input Text** → Raw text from the user
    2. **Preprocessing** → Lowercase, remove HTML/URLs/punctuation, tokenize, remove stopwords
    3. **TF-IDF Vectorization** → Convert cleaned text to a numerical feature vector
    4. **Multinomial Naive Bayes** → Compute P(class | features) using Bayes' Theorem
    5. **Prediction** → Return the class with the highest posterior probability
    6. **Probabilities** → `predict_proba()` gives confidence scores for all three classes

    ### Why Probabilities ≠ Guaranteed Accuracy
    The probability scores reflect the model's internal confidence based on training data patterns.
    They are **not** a guarantee of real-world accuracy. A 90% confidence means the model
    has seen many similar patterns in training that align with this prediction.
    """)
