"""
pages/1_Overview.py
===================
Home / Overview page — Social Media Sentiment Analysis System
Displays system introduction, KPI summary cards, and all 12 project modules.
"""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import init_db, get_prediction_stats
from src.icons import lucide
from src.train import load_metadata

init_db()

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; padding: 2.2rem 0 1rem;">
    <h1 style="font-size:2.4rem; font-weight:700; color:#ffffff; letter-spacing:-0.02em; margin-bottom:0.5rem; display:flex; align-items:center; justify-content:center; gap:12px;">
        {lucide('message-square', 32, '#818cf8')}
        <span>Social Media Sentiment Analysis</span>
    </h1>
    <p style="color:#94a3b8; font-size:1.05rem; max-width:640px; margin:0.6rem auto 0; font-weight:400; line-height:1.6;">
        Automatically classify social media text into Positive, Negative and Neutral sentiment using an end-to-end NLP pipeline.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── KPI Overview ──────────────────────────────────────────────────────────────
stats = get_prediction_stats()
meta  = load_metadata()

nb_metrics = meta.get("nb_metrics", {})
accuracy   = nb_metrics.get("accuracy", None)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Analyzed", f"{stats.get('total', 0):,}")
with col2:
    st.metric("Positive", f"{stats.get('positive', 0):,}",
              f"{stats.get('positive_pct', 0):.1f}%")
with col3:
    st.metric("Negative", f"{stats.get('negative', 0):,}",
              f"{stats.get('negative_pct', 0):.1f}%")
with col4:
    st.metric("Neutral",  f"{stats.get('neutral', 0):,}",
              f"{stats.get('neutral_pct', 0):.1f}%")
with col5:
    acc_display = f"{accuracy:.1%}" if accuracy else "Train first"
    st.metric("Model Accuracy", acc_display)

st.markdown("---")

# ── Module Cards ──────────────────────────────────────────────────────────────
st.markdown(f"""
<h3 style="color:#ffffff; font-size:1.35rem; font-weight:700; letter-spacing:-0.01em; margin-bottom:1rem; display:flex; align-items:center; gap:10px;">
    {lucide('layers', 22, '#818cf8')}
    <span>Project Modules</span>
</h3>
""", unsafe_allow_html=True)

modules = [
    ("1",  "database",       "Dataset Collection",     "Load, profile, and validate the sentiment dataset.",           "Dataset_Explorer"),
    ("2",  "search",         "EDA",                    "Explore distributions, word frequencies, and class balance.",  "Dataset_Explorer"),
    ("3",  "filter",         "Preprocessing",          "Clean text: remove HTML, URLs, stopwords, tokenize.",          "Dataset_Explorer"),
    ("4",  "target",         "TF-IDF Vectors",         "Convert text to numerical feature vectors.",                   "Dataset_Explorer"),
    ("5",  "cpu",            "Naive Bayes Model",      "Train Multinomial NB classifier on TF-IDF features.",          "Model_Evaluation"),
    ("6",  "bar-chart-2",    "Model Evaluation",       "Accuracy, F1, Confusion Matrix, Classification Report.",       "Model_Evaluation"),
    ("7",  "message-square", "Sentiment Analyzer",     "Analyze individual reviews in real time.",                     "Sentiment_Analyzer"),
    ("8",  "upload",         "Bulk CSV Analysis",      "Upload and analyze thousands of reviews at once.",             "Bulk_Analysis"),
    ("9",  "trending-up",    "Analytics Dashboard",    "Interactive KPI dashboard with Plotly charts.",               "Analytics"),
    ("10", "clock",          "Time Series Analysis",   "Daily trends, moving averages, exponential smoothing.",        "Analytics"),
    ("11", "history",        "Database Storage",       "SQLite prediction history with OLTP/OLAP concepts.",          "Prediction_History"),
    ("12", "book-open",      "Deployment & Documentation", "Load saved model; deploy to Streamlit Cloud.",          "About_Project"),
]

cols_per_row = 3
for i in range(0, len(modules), cols_per_row):
    row_cols = st.columns(cols_per_row)
    for j, col in enumerate(row_cols):
        if i + j < len(modules):
            num, icon_name, title, desc, url_path = modules[i + j]
            with col:
                st.markdown(f"""
                <a href="{url_path}" target="_self" class="module-card-link" style="text-decoration:none !important;">
                    <div class="card" style="min-height:130px; display:flex; flex-direction:column; justify-content:space-between; text-decoration:none !important;">
                        <div style="text-decoration:none !important;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem; text-decoration:none !important;">
                                <span style="font-size:0.75rem;color:#818cf8;font-weight:700;text-transform:uppercase;letter-spacing:0.1em; text-decoration:none !important;">
                                    Module {num}
                                </span>
                                {lucide(icon_name, 18, '#818cf8')}
                            </div>
                            <div style="font-size:1.05rem;font-weight:600;color:#f8fafc;margin-bottom:0.3rem; text-decoration:none !important;">{title}</div>
                            <div style="font-size:0.85rem;color:#94a3b8;line-height:1.4; text-decoration:none !important;">{desc}</div>
                        </div>
                    </div>
                </a>
                """, unsafe_allow_html=True)
