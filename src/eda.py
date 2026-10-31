"""
src/eda.py
==========
Module 2 – Exploratory Data Analysis

Computes statistical summaries and returns structured results
used by both the notebooks and the Streamlit dashboard.

Descriptive Statistics (Mean, Median, Mode, Variance, Std Dev)
Structured data exploration
Visualization as part of capstone project
"""

from collections import Counter
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from src.config import LABEL_COLUMN, SENTIMENT_CLASSES, TEXT_COLUMN


def compute_text_stats(df: pd.DataFrame, text_col: str = TEXT_COLUMN) -> Dict:
    """
    Compute detailed text-length statistics.

    Mean, Median, Mode, Variance, Standard Deviation,
                Min, Max, Percentiles.

    Args:
        df:       DataFrame with text column.
        text_col: Column name for text.

    Returns:
        dict of statistical measures.
    """
    lengths = df[text_col].dropna().str.len()
    word_counts = df[text_col].dropna().str.split().str.len()

    stats = {
        # Character-level stats
        "char_mean":    round(float(lengths.mean()), 2),
        "char_median":  float(lengths.median()),
        "char_mode":    int(lengths.mode()[0]) if not lengths.mode().empty else 0,
        "char_std":     round(float(lengths.std()), 2),
        "char_var":     round(float(lengths.var()), 2),
        "char_min":     int(lengths.min()),
        "char_max":     int(lengths.max()),
        "char_p25":     float(lengths.quantile(0.25)),
        "char_p75":     float(lengths.quantile(0.75)),
        "char_iqr":     float(lengths.quantile(0.75) - lengths.quantile(0.25)),

        # Word-level stats
        "word_mean":    round(float(word_counts.mean()), 2),
        "word_median":  float(word_counts.median()),
        "word_std":     round(float(word_counts.std()), 2),
        "word_min":     int(word_counts.min()),
        "word_max":     int(word_counts.max()),
    }
    return stats


def compute_class_distribution(df: pd.DataFrame) -> Dict:
    """
    Compute class frequency and percentage distribution.

    Frequency distributions, class balance analysis.
    """
    vc = df[LABEL_COLUMN].value_counts()
    total = len(df)
    return {
        "counts":  vc.to_dict(),
        "percent": (vc / total * 100).round(2).to_dict(),
        "total":   total,
    }


def compute_word_frequency(
    df: pd.DataFrame,
    text_col: str = "clean_text",
    sentiment: str = None,
    n: int = 30,
) -> pd.DataFrame:
    """
    Compute word frequency, optionally filtered by sentiment.

    Frequency analysis, term distribution.

    Args:
        df:        DataFrame with text and sentiment columns.
        text_col:  Column containing preprocessed text.
        sentiment: If set, filter to this sentiment class.
        n:         Return top N words.

    Returns:
        DataFrame with columns ['word', 'count'].
    """
    if sentiment:
        texts = df[df[LABEL_COLUMN] == sentiment][text_col].dropna()
    else:
        texts = df[text_col].dropna()

    all_words = texts.str.split().explode()
    freq = Counter(all_words)
    top_n = freq.most_common(n)
    return pd.DataFrame(top_n, columns=["word", "count"])


def compute_sentiment_text_stats(df: pd.DataFrame, text_col: str = TEXT_COLUMN) -> Dict:
    """
    Compute text length statistics broken down by sentiment class.

    Group-wise descriptive statistics.
    """
    result = {}
    for sentiment in SENTIMENT_CLASSES:
        subset = df[df[LABEL_COLUMN] == sentiment][text_col].dropna()
        if len(subset) == 0:
            continue
        lengths = subset.str.split().str.len()
        result[sentiment] = {
            "mean":   round(float(lengths.mean()), 2),
            "median": float(lengths.median()),
            "std":    round(float(lengths.std()), 2),
            "min":    int(lengths.min()),
            "max":    int(lengths.max()),
            "count":  int(len(subset)),
        }
    return result


def detect_class_imbalance(df: pd.DataFrame, threshold: float = 1.5) -> Dict:
    """
    Detect class imbalance using imbalance ratio.

    Imbalance Ratio = max_class_count / min_class_count.
    Ratio > threshold indicates imbalance.

    Returns:
        dict with is_imbalanced flag, ratio, and recommendation.
    """
    counts = df[LABEL_COLUMN].value_counts()
    ratio  = counts.max() / counts.min()
    is_imbalanced = ratio > threshold
    return {
        "is_imbalanced": is_imbalanced,
        "ratio":         round(float(ratio), 2),
        "threshold":     threshold,
        "max_class":     str(counts.idxmax()),
        "min_class":     str(counts.idxmin()),
        "recommendation": (
            "Use stratified splits and weighted metrics (weighted F1) "
            "to handle class imbalance."
        ) if is_imbalanced else "Class distribution is approximately balanced.",
    }


def get_full_eda_report(df: pd.DataFrame) -> Dict:
    """
    Run all EDA functions and return a consolidated report dictionary.

    This is the primary function called by the Dataset Explorer page.

    Capstone — EDA is the second phase of the DS Life Cycle.
    """
    clean_col = "clean_text" if "clean_text" in df.columns else TEXT_COLUMN

    report = {
        "total_records":    len(df),
        "total_columns":    len(df.columns),
        "columns":          list(df.columns),
        "missing":          df.isnull().sum().to_dict(),
        "duplicates":       int(df.duplicated(subset=[TEXT_COLUMN]).sum()),
        "class_dist":       compute_class_distribution(df),
        "text_stats":       compute_text_stats(df, text_col=TEXT_COLUMN),
        "imbalance":        detect_class_imbalance(df),
        "sentiment_stats":  compute_sentiment_text_stats(df, text_col=TEXT_COLUMN),
        "top_words_all":    compute_word_frequency(df, text_col=clean_col, n=30),
        "top_words_pos":    compute_word_frequency(df, text_col=clean_col,
                                                    sentiment="Positive", n=30),
        "top_words_neg":    compute_word_frequency(df, text_col=clean_col,
                                                    sentiment="Negative", n=30),
        "top_words_neu":    compute_word_frequency(df, text_col=clean_col,
                                                    sentiment="Neutral", n=30),
    }
    return report

