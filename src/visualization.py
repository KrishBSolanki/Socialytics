"""
src/visualization.py
====================
Shared visualisation helpers used across Streamlit pages.

All charts return Plotly figures for interactivity.
Static Matplotlib/Seaborn helpers are also provided for notebooks.

Visualization as the final presentation layer.
"""

from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.config import SENTIMENT_COLORS, SENTIMENT_CLASSES


# ── Colour Palette ────────────────────────────────────────────────────────────
_COLOR_SEQ = [
    SENTIMENT_COLORS["Positive"],
    SENTIMENT_COLORS["Negative"],
    SENTIMENT_COLORS["Neutral"],
]

PLOTLY_TEMPLATE = "plotly_dark"


def _fig_layout(fig, title: str = "", height: int = 400):
    """Apply consistent layout to all figures."""
    fig.update_layout(
        title        = dict(text=title, font=dict(size=16)),
        template     = PLOTLY_TEMPLATE,
        height       = height,
        margin       = dict(l=20, r=20, t=50, b=20),
        font         = dict(family="Lato, sans-serif", size=13),
        paper_bgcolor= "rgba(0,0,0,0)",
        plot_bgcolor = "rgba(0,0,0,0)",
    )
    return fig


# ── Sentiment Distribution Charts ────────────────────────────────────────────

def plot_sentiment_donut(dist_dict: Dict, title: str = "Sentiment Distribution") -> go.Figure:
    """
    Animated donut chart showing sentiment distribution.
    Proportional data visualisation.
    """
    labels = list(dist_dict.keys())
    values = list(dist_dict.values())
    colors = [SENTIMENT_COLORS.get(l, "#888") for l in labels]

    fig = go.Figure(go.Pie(
        labels     = labels,
        values     = values,
        hole       = 0.55,
        marker     = dict(colors=colors, line=dict(color="#1e1e2e", width=2)),
        textinfo   = "label+percent",
        hovertemplate = "%{label}: %{value:,} reviews (%{percent})<extra></extra>",
    ))
    _fig_layout(fig, title=title, height=350)
    fig.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.1))
    return fig


def plot_sentiment_bar(dist_dict: Dict, title: str = "Sentiment Count") -> go.Figure:
    """Vertical bar chart for sentiment counts."""
    labels = list(dist_dict.keys())
    values = list(dist_dict.values())
    colors = [SENTIMENT_COLORS.get(l, "#888") for l in labels]

    fig = go.Figure(go.Bar(
        x            = labels,
        y            = values,
        marker_color = colors,
        text         = [f"{v:,}" for v in values],
        textposition = "outside",
        hovertemplate = "%{x}: %{y:,}<extra></extra>",
    ))
    _fig_layout(fig, title=title, height=350)
    fig.update_layout(
        xaxis_title = "Sentiment",
        yaxis_title = "Number of Reviews",
        showlegend  = False,
    )
    return fig


def plot_probability_bar(prob_dict: Dict, title: str = "Prediction Probabilities") -> go.Figure:
    """Horizontal probability bar for single prediction display."""
    labels = list(prob_dict.keys())
    values = [v * 100 for v in prob_dict.values()]
    colors = [SENTIMENT_COLORS.get(l, "#888") for l in labels]

    fig = go.Figure(go.Bar(
        x            = values,
        y            = labels,
        orientation  = "h",
        marker_color = colors,
        text         = [f"{v:.1f}%" for v in values],
        textposition = "auto",
        hovertemplate = "%{y}: %{x:.2f}%<extra></extra>",
    ))
    _fig_layout(fig, title=title, height=250)
    fig.update_layout(
        xaxis = dict(title="Probability (%)", range=[0, 105]),
        yaxis = dict(title=""),
    )
    return fig


# ── Text Length Distribution ──────────────────────────────────────────────────

def plot_length_histogram(df: pd.DataFrame, col: str = "text",
                           title: str = "Review Length Distribution") -> go.Figure:
    """Histogram of word counts per review, coloured by sentiment."""
    df = df.copy()
    df["_len"] = df[col].str.split().str.len()

    fig = px.histogram(
        df, x="_len", color="sentiment",
        color_discrete_map = SENTIMENT_COLORS,
        nbins  = 40,
        barmode= "overlay",
        opacity= 0.75,
        labels = {"_len": "Word Count", "sentiment": "Sentiment"},
    )
    _fig_layout(fig, title=title, height=350)
    fig.update_layout(xaxis_title="Word Count", yaxis_title="Frequency")
    return fig


# ── Word Frequency ────────────────────────────────────────────────────────────

def plot_word_frequency(
    freq_df: pd.DataFrame,
    sentiment: str = "All",
    n: int = 20,
    title: str = None,
) -> go.Figure:
    """Horizontal bar chart for top word frequencies."""
    top = freq_df.head(n).copy()
    color = SENTIMENT_COLORS.get(sentiment, "#6366f1")
    title = title or f"Top {n} Words — {sentiment}"

    fig = go.Figure(go.Bar(
        x            = top["count"],
        y            = top["word"],
        orientation  = "h",
        marker_color = color,
        hovertemplate = "<b>%{y}</b>: %{x:,} occurrences<extra></extra>",
    ))
    _fig_layout(fig, title=title, height=max(300, n * 22))
    fig.update_layout(
        xaxis_title = "Frequency",
        yaxis       = dict(autorange="reversed"),
        showlegend  = False,
    )
    return fig


# ── Confusion Matrix Heatmap ──────────────────────────────────────────────────

def plot_confusion_matrix(cm_df: pd.DataFrame,
                           title: str = "Confusion Matrix") -> go.Figure:
    """
    Annotated heatmap for the confusion matrix.
    Model Evaluation visualisation.
    """
    labels = cm_df.columns.tolist()
    z      = cm_df.values

    text_labels = [[str(v) for v in row] for row in z]

    fig = go.Figure(go.Heatmap(
        z           = z,
        x           = labels,
        y           = labels,
        text        = text_labels,
        texttemplate= "<b>%{text}</b>",
        colorscale  = "Viridis",
        showscale   = True,
        hovertemplate = "Actual: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>",
    ))
    _fig_layout(fig, title=title, height=400)
    fig.update_layout(
        xaxis_title = "Predicted Label",
        yaxis_title = "Actual Label",
    )
    return fig


# ── Time Series Charts ────────────────────────────────────────────────────────

def plot_sentiment_trend(
    df: pd.DataFrame,
    date_col: str = "date",
    title: str = "Daily Sentiment Trend",
) -> go.Figure:
    """
    Line chart showing daily sentiment counts over time.
    Time Series Analysis.
    """
    fig = go.Figure()
    for sentiment in SENTIMENT_CLASSES:
        if sentiment in df.columns:
            fig.add_trace(go.Scatter(
                x    = df[date_col],
                y    = df[sentiment],
                mode = "lines+markers",
                name = sentiment,
                line = dict(color=SENTIMENT_COLORS[sentiment], width=2),
                hovertemplate = f"<b>{sentiment}</b><br>Date: %{{x}}<br>Count: %{{y}}<extra></extra>",
            ))
    _fig_layout(fig, title=title, height=380)
    fig.update_layout(xaxis_title="Date", yaxis_title="Count",
                      hovermode="x unified", showlegend=True)
    return fig


def plot_moving_average(
    series: pd.Series,
    window: int = 7,
    sentiment: str = "Positive",
    title: str = None,
) -> go.Figure:
    """
    Plot raw counts and moving average for one sentiment class.
    Moving Average smoothing.
    """
    ma = series.rolling(window=window, center=True).mean()
    color = SENTIMENT_COLORS.get(sentiment, "#6366f1")
    title = title or f"{sentiment} Sentiment — {window}-Day Moving Average"

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=series.index, y=series.values,
        name="Daily Count",
        marker_color=color, opacity=0.35,
    ))
    fig.add_trace(go.Scatter(
        x=ma.index, y=ma.values,
        mode="lines", name=f"{window}-Day MA",
        line=dict(color=color, width=2.5),
    ))
    _fig_layout(fig, title=title, height=350)
    fig.update_layout(xaxis_title="Date", yaxis_title="Count",
                      bargap=0.05)
    return fig


# ── Metrics Summary Chart ─────────────────────────────────────────────────────

def plot_metrics_radar(metrics: dict, title: str = "Model Performance") -> go.Figure:
    """Radar chart for model evaluation metrics."""
    categories = ["Accuracy", "Precision\n(Macro)", "Recall\n(Macro)", "F1\n(Macro)"]
    values = [
        metrics.get("accuracy", 0),
        metrics.get("precision_macro", 0),
        metrics.get("recall_macro", 0),
        metrics.get("f1_macro", 0),
    ]
    values_pct = [v * 100 for v in values]

    fig = go.Figure(go.Scatterpolar(
        r      = values_pct + [values_pct[0]],
        theta  = categories + [categories[0]],
        fill   = "toself",
        name   = "Naive Bayes",
        line   = dict(color="#6366f1"),
        fillcolor = "rgba(99,102,241,0.3)",
    ))
    _fig_layout(fig, title=title, height=380)
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
    )
    return fig


def plot_model_comparison(nb_metrics: dict, lr_metrics: dict,
                           title: str = "NB vs Logistic Regression") -> go.Figure:
    """Grouped bar chart comparing two models across metrics."""
    metric_names = ["Accuracy", "Precision (Macro)", "Recall (Macro)", "F1 (Macro)"]
    nb_vals = [
        nb_metrics.get("accuracy", 0) * 100,
        nb_metrics.get("precision_macro", 0) * 100,
        nb_metrics.get("recall_macro", 0) * 100,
        nb_metrics.get("f1_macro", 0) * 100,
    ]
    lr_vals = [
        lr_metrics.get("accuracy", 0) * 100,
        lr_metrics.get("precision_macro", 0) * 100,
        lr_metrics.get("recall_macro", 0) * 100,
        lr_metrics.get("f1_macro", 0) * 100,
    ]

    fig = go.Figure([
        go.Bar(name="Naive Bayes", x=metric_names, y=nb_vals,
               marker_color="#6366f1",
               text=[f"{v:.1f}%" for v in nb_vals], textposition="outside"),
        go.Bar(name="Logistic Regression", x=metric_names, y=lr_vals,
               marker_color="#10b981",
               text=[f"{v:.1f}%" for v in lr_vals], textposition="outside"),
    ])
    _fig_layout(fig, title=title, height=380)
    fig.update_layout(
        barmode     = "group",
        yaxis       = dict(title="Score (%)", range=[0, 115]),
        xaxis_title = "Metric",
    )
    return fig

