"""
pages/6_Model_Evaluation.py
============================
Module 6 – Model Evaluation

Displays comprehensive evaluation metrics, confusion matrix heatmap,
classification report, cross-validation results, and NB vs LR comparison.
"""

import os
import sys

import numpy as np
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import SENTIMENT_CLASSES
from src.train import load_metadata
from src.evaluation import confusion_matrix_df, metrics_explanation
from src.visualization import (
    plot_confusion_matrix, plot_metrics_radar, plot_model_comparison,
)
from src.icons import lucide

st.markdown(f"""
<h1 style="color:#ffffff; font-size:2rem; font-weight:700; letter-spacing:-0.02em; margin-bottom:0.25rem; display:flex; align-items:center; gap:10px;">
    {lucide('bar-chart-2', 26, '#818cf8')}
    <span>Model Evaluation</span>
</h1>
<p style="color:#94a3b8; font-size:1rem; margin-top:0;">Comprehensive evaluation of the Multinomial Naive Bayes classifier.</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Load Metadata ─────────────────────────────────────────────────────────────
meta = load_metadata()

if not meta:
    st.error("""
    **Model metadata not found.**
    Please train the model first:
    ```bash
    python train_model.py
    ```
    """)
    st.stop()

nb_metrics = meta.get("nb_metrics", {})
lr_metrics = meta.get("lr_metrics", {})

if not nb_metrics:
    st.warning("No evaluation metrics found in metadata. Please retrain the model.")
    st.stop()

# ════════════════════════════════════════════════════════════════════════════════
# SCALAR METRICS KPI
# ════════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<h3 style="color:#ffffff; font-size:1.25rem; font-weight:700; margin-bottom:1rem; display:flex; align-items:center; gap:8px;">
    {lucide('target', 20, '#818cf8')}
    <span>Naive Bayes — Overall Performance</span>
</h3>
""", unsafe_allow_html=True)

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Accuracy",          f"{nb_metrics.get('accuracy',0):.2%}")
m2.metric("F1 (Macro)",        f"{nb_metrics.get('f1_macro',0):.2%}")
m3.metric("F1 (Weighted)",     f"{nb_metrics.get('f1_weighted',0):.2%}")
m4.metric("Precision (Macro)", f"{nb_metrics.get('precision_macro',0):.2%}")
m5.metric("Recall (Macro)",    f"{nb_metrics.get('recall_macro',0):.2%}")
m6.metric("Training Samples",  f"{meta.get('training_samples', 'N/A'):,}"
          if isinstance(meta.get("training_samples"), int) else "N/A")

st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════════
# CONFUSION MATRIX + RADAR
# ════════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<h3 style="color:#ffffff; font-size:1.25rem; font-weight:700; margin-bottom:1rem; display:flex; align-items:center; gap:8px;">
    {lucide('layers', 20, '#818cf8')}
    <span>Confusion Matrix &amp; Radar Chart</span>
</h3>
""", unsafe_allow_html=True)

col_cm, col_radar = st.columns(2)

with col_cm:
    cm_data = nb_metrics.get("confusion_matrix")
    labels  = nb_metrics.get("labels", SENTIMENT_CLASSES)
    if cm_data:
        cm_array = np.array(cm_data)
        cm_df    = pd.DataFrame(cm_array, index=labels, columns=labels)
        fig_cm   = plot_confusion_matrix(cm_df)
        st.plotly_chart(fig_cm, use_container_width=True)

        st.caption("""
        **Reading the Confusion Matrix:**
        - **Rows** = Actual sentiment class
        - **Columns** = Predicted sentiment class
        - **Diagonal** = Correct predictions
        - **Off-diagonal** = Misclassifications
        """)
    else:
        st.info("Confusion matrix not available. Retrain the model.")

with col_radar:
    fig_radar = plot_metrics_radar(nb_metrics)
    st.plotly_chart(fig_radar, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# CLASSIFICATION REPORT
# ════════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(f"""
<h3 style="color:#ffffff; font-size:1.25rem; font-weight:700; margin-bottom:1rem; display:flex; align-items:center; gap:8px;">
    {lucide('file-text', 20, '#818cf8')}
    <span>Classification Report (Per-Class Breakdown)</span>
</h3>
""", unsafe_allow_html=True)

report = nb_metrics.get("classification_report", {})
if report:
    rows = []
    for label in labels:
        if label in report:
            r = report[label]
            rows.append({
                "Class":     label,
                "Precision": f"{r.get('precision',0):.4f}",
                "Recall":    f"{r.get('recall',0):.4f}",
                "F1-Score":  f"{r.get('f1-score',0):.4f}",
                "Support":   int(r.get("support", 0)),
            })
    # Add averages
    for avg_key in ["macro avg", "weighted avg"]:
        if avg_key in report:
            r = report[avg_key]
            rows.append({
                "Class":     avg_key.title(),
                "Precision": f"{r.get('precision',0):.4f}",
                "Recall":    f"{r.get('recall',0):.4f}",
                "F1-Score":  f"{r.get('f1-score',0):.4f}",
                "Support":   int(r.get("support", 0)),
            })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════════
# MODEL COMPARISON (NB vs LR)
# ════════════════════════════════════════════════════════════════════════════════
if lr_metrics:
    st.markdown("---")
    st.markdown(f"""
    <h3 style="color:#ffffff; font-size:1.25rem; font-weight:700; margin-bottom:0.25rem; display:flex; align-items:center; gap:8px;">
        {lucide('cpu', 20, '#818cf8')}
        <span>Model Comparison: Naive Bayes vs Logistic Regression</span>
    </h3>
    """, unsafe_allow_html=True)
    st.caption("Logistic Regression uses gradient descent optimization. Naive Bayes uses direct probability estimation.")

    fig_comp = plot_model_comparison(nb_metrics, lr_metrics)
    st.plotly_chart(fig_comp, use_container_width=True)

    comp_data = {
        "Model":           ["Multinomial Naive Bayes", "Logistic Regression"],
        "Accuracy":        [f"{nb_metrics.get('accuracy',0):.4f}",
                            f"{lr_metrics.get('accuracy',0):.4f}"],
        "F1 Macro":        [f"{nb_metrics.get('f1_macro',0):.4f}",
                            f"{lr_metrics.get('f1_macro',0):.4f}"],
        "F1 Weighted":     [f"{nb_metrics.get('f1_weighted',0):.4f}",
                            f"{lr_metrics.get('f1_weighted',0):.4f}"],
        "Optimization":    ["Direct Probability (No GD)", "L-BFGS Gradient Descent"],
        "Training Speed":  ["Fast Analytical", "Iterative Gradient Steps"],
    }
    st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════════
# METRICS EXPLANATION
# ════════════════════════════════════════════════════════════════════════════════
st.markdown("---")
with st.expander("Evaluation Metrics Explained"):
    st.markdown(metrics_explanation())

# ════════════════════════════════════════════════════════════════════════════════
# OPTIMIZATION THEORY
# ════════════════════════════════════════════════════════════════════════════════
with st.expander("Optimization — Gradient Descent"):
    st.markdown("""
    ### Optimization in Machine Learning

    **Objective Function / Loss Function**
    Most ML models minimize a loss function $L(\\theta)$ that measures prediction error.

    **Batch Gradient Descent:**
    $$\\theta := \\theta - \\eta \\cdot \\nabla_\\theta L(\\theta)$$
    Uses the entire training dataset to compute gradients.

    **Stochastic Gradient Descent (SGD):**
    $$\\theta := \\theta - \\eta \\cdot \\nabla_\\theta L(\\theta; x^{(i)}, y^{(i)})$$
    Updates parameters using ONE sample at a time. Noisy but faster.

    **Mini-Batch Gradient Descent:**
    A compromise — uses a small batch of samples per update.

    ---

    **Why Naive Bayes does NOT use Gradient Descent:**

    Multinomial Naive Bayes computes parameters analytically using counting:
    $$P(w | C_k) = \\frac{\\text{count}(w, C_k) + \\alpha}{\\sum_w \\text{count}(w, C_k) + \\alpha|V|}$$

    There is no cost function to minimize iteratively.
    Logistic Regression, on the other hand, minimizes cross-entropy loss via L-BFGS,
    which IS a gradient-based optimization algorithm.

    **Hyperparameter Tuning:**
    - NB: `alpha` (Laplace smoothing) — controls smoothing strength
    - TF-IDF: `max_features`, `ngram_range` — feature engineering choices
    - LR: `C` (regularization), `max_iter` (convergence budget)
    """)
