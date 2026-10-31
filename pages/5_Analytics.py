"""
pages/5_Analytics.py
====================
Module 9 – Analytics Dashboard + Module 10 – Time Series Analysis

Interactive dashboard with KPI cards, Plotly charts,
daily sentiment trends, moving averages, and filters.
"""

import os
import sys
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import SENTIMENT_COLORS, SENTIMENT_CLASSES, LABEL_COLUMN, TIMESTAMP_COLUMN
from src.data_loader import load_dataset
from src.database import fetch_all_predictions, get_prediction_stats
from src.icons import lucide
from src.train import load_metadata
from src.visualization import (
    plot_sentiment_donut, plot_sentiment_bar,
    plot_length_histogram, plot_sentiment_trend,
    plot_moving_average, plot_word_frequency,
)

st.markdown(f"""
<h1 style="color:#ffffff; font-size:2rem; font-weight:700; letter-spacing:-0.02em; margin-bottom:0.25rem; display:flex; align-items:center; gap:10px;">
    {lucide('trending-up', 26, '#818cf8')}
    <span>Analytics Dashboard</span>
</h1>
<p style="color:#94a3b8; font-size:1rem; margin-top:0;">Interactive sentiment analytics with time series insights.</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading dataset...")
def load_data():
    df = load_dataset()
    meta = load_metadata()
    return df, meta

df_raw, meta = load_data()
pred_stats   = get_prediction_stats()
nb_metrics   = meta.get("nb_metrics", {})

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:0.5rem;">
        {lucide('filter', 18, '#818cf8')}
        <span style="font-size:1.05rem; font-weight:700; color:#f8fafc;">Dashboard Filters</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Sentiment filter
    sent_filter = st.multiselect(
        "Sentiment:",
        options=SENTIMENT_CLASSES,
        default=SENTIMENT_CLASSES,
    )

    # Date range filter (if timestamps exist)
    has_dates = TIMESTAMP_COLUMN in df_raw.columns
    if has_dates:
        df_raw[TIMESTAMP_COLUMN] = pd.to_datetime(df_raw[TIMESTAMP_COLUMN], errors="coerce")
        valid_dates = df_raw[TIMESTAMP_COLUMN].dropna()
        if len(valid_dates) > 0:
            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()
            date_range = st.date_input(
                "Date Range:",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
            )
        else:
            has_dates = False

    # Source filter
    if "source" in df_raw.columns:
        sources = ["All"] + df_raw["source"].unique().tolist()
        src_filter = st.selectbox("Data Source:", sources)
    else:
        src_filter = "All"

    st.markdown("---")
    st.caption("Filters apply to dataset charts below.")

# ── Apply Filters ─────────────────────────────────────────────────────────────
df_filtered = df_raw[df_raw[LABEL_COLUMN].isin(sent_filter)].copy()
if has_dates and len(date_range) == 2:
    df_filtered = df_filtered[
        (df_filtered[TIMESTAMP_COLUMN].dt.date >= date_range[0]) &
        (df_filtered[TIMESTAMP_COLUMN].dt.date <= date_range[1])
    ]
if src_filter != "All" and "source" in df_filtered.columns:
    df_filtered = df_filtered[df_filtered["source"] == src_filter]

# ════════════════════════════════════════════════════════════════════════════════
# KPI SECTION
# ════════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<h3 style="color:#ffffff; font-size:1.25rem; font-weight:700; margin-bottom:1rem; display:flex; align-items:center; gap:8px;">
    {lucide('target', 20, '#818cf8')}
    <span>Key Performance Indicators</span>
</h3>
""", unsafe_allow_html=True)

dist = df_filtered[LABEL_COLUMN].value_counts()
total = len(df_filtered)

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Reviews",  f"{total:,}")
k2.metric("Positive",       f"{dist.get('Positive',0):,}",
          f"{dist.get('Positive',0)/total*100:.1f}%" if total else "—")
k3.metric("Negative",       f"{dist.get('Negative',0):,}",
          f"{dist.get('Negative',0)/total*100:.1f}%" if total else "—")
k4.metric("Neutral",        f"{dist.get('Neutral',0):,}",
          f"{dist.get('Neutral',0)/total*100:.1f}%" if total else "—")
k5.metric("Positive %",
          f"{dist.get('Positive',0)/total*100:.1f}%" if total else "—")
k6.metric("Model Accuracy",
          f"{nb_metrics.get('accuracy',0):.1%}" if nb_metrics else "N/A")

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════════
# CHARTS — Row 1: Distribution
# ════════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<h3 style="color:#ffffff; font-size:1.25rem; font-weight:700; margin-bottom:1rem; display:flex; align-items:center; gap:8px;">
    {lucide('bar-chart-2', 20, '#818cf8')}
    <span>Sentiment Distribution</span>
</h3>
""", unsafe_allow_html=True)

r1c1, r1c2 = st.columns(2)

with r1c1:
    if total > 0:
        fig_donut = plot_sentiment_donut(dist.to_dict(), "Sentiment Distribution (Donut)")
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("No data matches current filters.")

with r1c2:
    if total > 0:
        fig_bar = plot_sentiment_bar(dist.to_dict(), "Sentiment Count Comparison")
        st.plotly_chart(fig_bar, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# CHARTS — Row 2: Time Series Analysis
# ════════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<h3 style="color:#ffffff; font-size:1.25rem; font-weight:700; margin-bottom:1rem; display:flex; align-items:center; gap:8px;">
    {lucide('clock', 20, '#818cf8')}
    <span>Time Series Analysis</span>
</h3>
""", unsafe_allow_html=True)

if has_dates and total > 0 and TIMESTAMP_COLUMN in df_filtered.columns:
    df_ts = df_filtered.copy()
    df_ts["date"] = df_ts[TIMESTAMP_COLUMN].dt.date

    # Daily pivot
    daily = df_ts.groupby(["date", LABEL_COLUMN]).size().unstack(fill_value=0)
    for s in SENTIMENT_CLASSES:
        if s not in daily.columns:
            daily[s] = 0
    daily = daily.reset_index()
    daily["date"] = pd.to_datetime(daily["date"])
    daily = daily.sort_values("date")

    # Trend chart
    fig_trend = plot_sentiment_trend(daily, date_col="date", title="Daily Sentiment Trend")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")
    st.markdown(f"""
    <h3 style="color:#ffffff; font-size:1.25rem; font-weight:700; margin-bottom:1rem; display:flex; align-items:center; gap:8px;">
        {lucide('trending-up', 20, '#818cf8')}
        <span>Moving Average Trend</span>
    </h3>
    """, unsafe_allow_html=True)
    ma_col = st.selectbox("Sentiment for Moving Average:", SENTIMENT_CLASSES, key="ma_sent")
    ma_win = st.slider("Window Size (days):", 3, 30, 7)

    if ma_col in daily.columns:
        series = daily.set_index("date")[ma_col]
        fig_ma = plot_moving_average(series, window=ma_win, sentiment=ma_col)
        st.plotly_chart(fig_ma, use_container_width=True)

    # Exponential Smoothing explanation
    with st.expander("Exponential Smoothing & ARIMA"):
        st.markdown("""
        ### Exponential Smoothing

        Simple Exponential Smoothing assigns exponentially decreasing weights to past observations:

        $$\\hat{y}_{t+1} = \\alpha \\cdot y_t + (1 - \\alpha) \\cdot \\hat{y}_t$$

        Where:
        - $\\alpha \\in (0, 1)$ is the smoothing factor
        - Higher $\\alpha$ -> more weight on recent observations (reactive)
        - Lower $\\alpha$ -> smoother, relies more on history (stable)

        ---

        ### ARIMA (AutoRegressive Integrated Moving Average)

        **AR(p)**: The variable depends on its own past *p* values.
        **I(d)**: Differencing to make the series stationary.
        **MA(q)**: The variable depends on past *q* forecast errors.

        $$y_t = c + \\phi_1 y_{t-1} + \\cdots + \\phi_p y_{t-p} + \\theta_1 \\epsilon_{t-1} + \\cdots + \\theta_q \\epsilon_{t-q} + \\epsilon_t$$

        **SARIMA** extends ARIMA with seasonal components (S, P, D, Q, m).

        > **Note:** ARIMA forecasting on this dataset is conceptual.
        > Reliable forecasts require >= 50 chronological observations per class.
        """)

else:
    st.info("Time series charts require timestamp data. The current dataset includes synthetic dates.")
    if total > 0 and TIMESTAMP_COLUMN in df_raw.columns:
        df_ts = df_raw.copy()
        df_ts[TIMESTAMP_COLUMN] = pd.to_datetime(df_ts[TIMESTAMP_COLUMN], errors="coerce")
        df_ts = df_ts.dropna(subset=[TIMESTAMP_COLUMN])
        df_ts["date"] = df_ts[TIMESTAMP_COLUMN].dt.date
        daily = df_ts.groupby(["date", LABEL_COLUMN]).size().unstack(fill_value=0)
        for s in SENTIMENT_CLASSES:
            if s not in daily.columns:
                daily[s] = 0
        daily = daily.reset_index()
        daily["date"] = pd.to_datetime(daily["date"])
        daily = daily.sort_values("date")
        fig_trend = plot_sentiment_trend(daily, date_col="date",
                                          title="Daily Sentiment Trend (Synthetic Timestamps)")
        st.plotly_chart(fig_trend, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# CHARTS — Row 3: Length + Prediction History Stats
# ════════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<h3 style="color:#ffffff; font-size:1.25rem; font-weight:700; margin-bottom:1rem; display:flex; align-items:center; gap:8px;">
    {lucide('file-text', 20, '#818cf8')}
    <span>Review Length Distribution</span>
</h3>
""", unsafe_allow_html=True)

if total > 0:
    from src.config import TEXT_COLUMN
    fig_hist = plot_length_histogram(df_filtered, col=TEXT_COLUMN)
    st.plotly_chart(fig_hist, use_container_width=True)

# Prediction history stats
if pred_stats.get("total", 0) > 0:
    st.markdown("---")
    st.markdown(f"""
    <h3 style="color:#ffffff; font-size:1.25rem; font-weight:700; margin-bottom:1rem; display:flex; align-items:center; gap:8px;">
        {lucide('history', 20, '#818cf8')}
        <span>Prediction History (from Database)</span>
    </h3>
    """, unsafe_allow_html=True)
    ph1, ph2, ph3, ph4 = st.columns(4)
    ph1.metric("Total Predictions", f"{pred_stats['total']:,}")
    ph2.metric("Positive",          f"{pred_stats.get('positive', 0):,}")
    ph3.metric("Negative",          f"{pred_stats.get('negative', 0):,}")
    ph4.metric("Neutral",           f"{pred_stats.get('neutral', 0):,}")
