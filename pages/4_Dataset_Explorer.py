"""
pages/4_Dataset_Explorer.py
============================
Modules 1, 2, 3, 4 — Dataset, EDA, Preprocessing, TF-IDF

Provides full exploratory data analysis with interactive visualizations,
preprocessing pipeline demo, and TF-IDF explanation.
"""

import os
import sys

import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import SENTIMENT_COLORS, SENTIMENT_CLASSES, TEXT_COLUMN, LABEL_COLUMN
from src.data_loader import load_dataset, get_dataset_profile
from src.preprocessing import preprocess_dataframe, clean_text, get_preprocessing_stats
from src.eda import get_full_eda_report, compute_text_stats
from src.visualization import (
    plot_sentiment_donut, plot_sentiment_bar,
    plot_length_histogram, plot_word_frequency,
)
from src.feature_extraction import tfidf_math_explanation
from src.icons import lucide

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<h1 style="color:#ffffff; font-size:2rem; font-weight:700; letter-spacing:-0.02em; margin-bottom:0.25rem; display:flex; align-items:center; gap:10px;">
    {lucide('search', 26, '#818cf8')}
    <span>Dataset Explorer</span>
</h1>
<p style="color:#94a3b8; font-size:1rem; margin-top:0;">Explore the dataset, perform EDA, and understand the preprocessing pipeline.</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading and preprocessing dataset...")
def load_and_preprocess():
    df_raw = load_dataset()
    df_clean = preprocess_dataframe(df_raw)
    return df_raw, df_clean

df_raw, df_clean = load_and_preprocess()
profile = get_dataset_profile(df_raw)
eda     = get_full_eda_report(df_clean)

# ── Navigation Tabs ───────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Dataset Profile",
    "EDA & Statistics",
    "Word Clouds",
    "Preprocessing",
    "TF-IDF Vectors",
])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — Dataset Profile
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Dataset Profile (Module 1)")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Records",  f"{profile['n_rows']:,}")
    m2.metric("Total Columns",  profile["n_cols"])
    m3.metric("Duplicates",     f"{profile['duplicates']:,}")
    m4.metric("Memory",         f"{profile['memory_mb']} MB")

    st.markdown("---")

    # Class distribution
    if "class_distribution" in profile:
        st.subheader("Class Distribution")
        dist = profile["class_distribution"]
        pct  = profile["class_pct"]

        d_cols = st.columns(3)
        for i, sentiment in enumerate(["Positive", "Negative", "Neutral"]):
            count = dist.get(sentiment, 0)
            p     = pct.get(sentiment, 0)
            c     = SENTIMENT_COLORS[sentiment]
            with d_cols[i]:
                st.markdown(f"""
                <div style="padding:1rem;background:{c}15;border:1px solid {c}40;
                            border-radius:12px;text-align:center;">
                    <div style="font-size:.8rem;color:#94a3b8;">{sentiment}</div>
                    <div style="font-size:1.8rem;font-weight:700;color:{c};">{count:,}</div>
                    <div style="font-size:.85rem;color:#94a3b8;">{p}%</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Column Info")
        dtype_df = pd.DataFrame({
            "Column": list(profile["dtypes"].keys()),
            "Type":   list(profile["dtypes"].values()),
            "Missing":list(profile["missing"].values()),
            "Missing %": list(profile["missing_pct"].values()),
        })
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    with col_right:
        st.subheader("Sample Records")
        st.dataframe(df_raw[[TEXT_COLUMN, LABEL_COLUMN]].sample(8, random_state=42),
                     use_container_width=True, hide_index=True)

    # Text stats
    st.markdown("---")
    st.subheader("Text Length Statistics")
    ts = profile
    s1, s2, s3, s4, s5, s6 = st.columns(6)
    s1.metric("Avg Words",    ts.get("word_count_mean", "—"))
    s2.metric("Std Dev",      ts.get("word_count_std",  "—"))
    s3.metric("Min Words",    ts.get("word_count_min",  "—"))
    s4.metric("Max Words",    ts.get("word_count_max",  "—"))
    s5.metric("Median Words", ts.get("word_count_median","—"))
    s6.metric("Classes",      ts.get("n_classes", "—"))

    # Imbalance alert
    imb = eda["imbalance"]
    if imb["is_imbalanced"]:
        st.warning(
            f"Class Imbalance Detected — Imbalance Ratio: {imb['ratio']:.2f}x  "
            f"(Most: {imb['max_class']}, Least: {imb['min_class']})\n\n"
            f"Recommendation: {imb['recommendation']}"
        )
    else:
        st.success(f"Classes are well-balanced (Ratio: {imb['ratio']:.2f}x)")


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — EDA & Statistics
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Exploratory Data Analysis (Module 2)")

    dist_counts = eda["class_dist"]["counts"]
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(plot_sentiment_donut(dist_counts), use_container_width=True)
    with c2:
        st.plotly_chart(plot_sentiment_bar(dist_counts), use_container_width=True)

    st.markdown("---")
    st.subheader("Review Length Distribution")
    st.plotly_chart(plot_length_histogram(df_clean, col=TEXT_COLUMN),
                    use_container_width=True)

    st.markdown("---")
    st.subheader("Descriptive Statistics per Sentiment")
    stats_rows = []
    for sentiment, s in eda["sentiment_stats"].items():
        stats_rows.append({
            "Sentiment": sentiment,
            "Count":     s["count"],
            "Mean Words":s["mean"],
            "Std Dev":   s["std"],
            "Median":    s["median"],
            "Min":       s["min"],
            "Max":       s["max"],
        })
    if stats_rows:
        st.dataframe(pd.DataFrame(stats_rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Top Words by Sentiment")
    sent_filter = st.selectbox("Select Sentiment:", ["All"] + SENTIMENT_CLASSES, key="word_sent")
    n_words     = st.slider("Number of words:", 10, 40, 20, key="n_words")

    key_map = {
        "All":      "top_words_all",
        "Positive": "top_words_pos",
        "Negative": "top_words_neg",
        "Neutral":  "top_words_neu",
    }
    word_df = eda[key_map[sent_filter]]
    fig_wf  = plot_word_frequency(word_df, sentiment=sent_filter, n=n_words)
    st.plotly_chart(fig_wf, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — Word Clouds
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Sentiment Word Clouds")
    st.caption("Word clouds visualise the most frequent terms per sentiment class.")

    wc_cols = st.columns(3)
    wc_config = [
        ("Positive", "#10b981", eda["top_words_pos"]),
        ("Negative", "#ef4444", eda["top_words_neg"]),
        ("Neutral",  "#6366f1", eda["top_words_neu"]),
    ]

    for col, (sentiment, color, freq_df) in zip(wc_cols, wc_config):
        with col:
            st.markdown(f"**{sentiment}**")
            if len(freq_df) > 0:
                freq_dict = dict(zip(freq_df["word"], freq_df["count"]))
                wc = WordCloud(
                    width=400, height=300,
                    background_color="black",
                    colormap="Set2",
                    max_words=80,
                    prefer_horizontal=0.85,
                ).generate_from_frequencies(freq_dict)
                fig_wc, ax = plt.subplots(figsize=(5, 3.5))
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                fig_wc.patch.set_facecolor("#0d0d1a")
                st.pyplot(fig_wc, use_container_width=True)
                plt.close()
            else:
                st.info("Not enough data to generate word cloud.")


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — Preprocessing Demo
# ════════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Text Preprocessing Pipeline (Module 3)")

    st.markdown("""
    The preprocessing pipeline transforms raw text into clean, normalised tokens
    ready for feature extraction. Each step is designed to reduce noise while
    preserving sentiment-critical information (especially negation words).
    """)

    steps = [
        ("1", "Lowercase",          "Convert all text to lowercase.",                            "I LOVE this product!",          "i love this product!"),
        ("2", "HTML Tag Removal",   "Remove `<br>`, `<b>`, `<p>` etc.",                         "<p>Great product!</p>",         "great product!"),
        ("3", "URL Removal",        "Remove http://, https://, www links.",                      "Visit https://example.com now", "visit now"),
        ("4", "Mention & Hashtag",  "Remove @user, expand #hashtag.",                           "@john loved #product",          "john loved product"),
        ("5", "Punctuation",        "Remove special characters.",                                "Amazing product!!!",            "amazing product"),
        ("6", "Tokenization",       "Split text into individual word tokens.",                   "amazing product",               "['amazing', 'product']"),
        ("7", "Stopword Removal",   "Remove common words (keep negations like 'not', 'never')", "this is a great product",       "great product"),
        ("8", "Short Token Filter", "Remove tokens with fewer than 2 characters.",              "i a great product",             "great product"),
    ]

    st.markdown("#### Pipeline Steps")
    pipe_df = pd.DataFrame(steps, columns=["Step", "Name", "Description", "Before", "After"])
    st.dataframe(pipe_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### Live Preprocessing Demo")
    demo_text = st.text_area(
        "Enter text to preprocess:",
        value="<b>Absolutely LOVE</b> this product! Visit https://buy.now @seller #amazing product",
        height=80,
        key="preprocess_demo",
    )
    if demo_text:
        cleaned = clean_text(demo_text)
        dc1, dc2 = st.columns(2)
        with dc1:
            st.markdown("**Raw Text:**")
            st.code(demo_text, language="text")
        with dc2:
            st.markdown("**Cleaned Text:**")
            st.code(cleaned, language="text")

    st.markdown("---")
    pre_stats = get_preprocessing_stats(df_raw, df_clean)
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Raw Records",    f"{pre_stats['raw_records']:,}")
    p2.metric("Clean Records",  f"{pre_stats['clean_records']:,}")
    p3.metric("Removed",        f"{pre_stats['records_removed']:,}")
    p4.metric("Vocab Reduction",f"{pre_stats['vocab_raw'] - pre_stats['vocab_clean']:,}")


# ════════════════════════════════════════════════════════════════════════════════
# TAB 5 — TF-IDF
# ════════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("TF-IDF Feature Extraction (Module 4)")
    st.markdown(tfidf_math_explanation())

    st.markdown("---")
    st.subheader("TF-IDF Parameters Used in This Project")
    param_data = {
        "Parameter":   ["max_features", "min_df", "max_df", "ngram_range", "sublinear_tf", "smooth_idf"],
        "Value":       ["20,000", "2", "0.95", "(1, 2)", "True", "True"],
        "Explanation": [
            "Keep top 20,000 features by TF-IDF score",
            "Ignore words appearing in fewer than 2 documents",
            "Ignore words appearing in more than 95% of documents",
            "Use unigrams AND bigrams (e.g. 'not good' as one feature)",
            "Apply log(1+TF) to dampen high-frequency terms",
            "Add 1 to avoid zero-division in IDF",
        ]
    }
    st.dataframe(pd.DataFrame(param_data), use_container_width=True, hide_index=True)

    st.markdown("---")
    with st.expander("TruncatedSVD / LSA Dimensionality Reduction"):
        st.markdown("""
        **Latent Semantic Analysis (LSA) using TruncatedSVD**

        After TF-IDF creates a sparse document-term matrix **X** of shape *(n_docs × vocab_size)*,
        we can optionally apply **Singular Value Decomposition** to reduce dimensionality:

        $$X \\approx U \\Sigma V^T$$

        - **U**: document-concept matrix (n_docs × k)
        - **Σ**: diagonal matrix of singular values (importance of each concept)
        - **V^T**: concept-term matrix (k × vocab_size)

        **Eigenvalues** (Σ²) represent the variance explained by each latent dimension.
        Keeping top-k components captures the most important semantic patterns.

        This is implemented in `src/feature_extraction.py` as `perform_svd_analysis()`.
        """)
