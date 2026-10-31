"""
src/data_loader.py
==================
Module 1 – Dataset Collection & Loading

Handles:
  • Automatic dataset generation (seed-controlled, reproducible)
  • Manual CSV loading
  • Basic dataset validation and profiling
  • Class imbalance detection

Data Science Life Cycle — Data Collection stage
Structured vs unstructured data
Missing values, duplicates, data integrity
"""

import os
import json
import random
import sqlite3
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from src.config import (
    RAW_CSV, PROCESSED_CSV, TEXT_COLUMN, LABEL_COLUMN,
    TIMESTAMP_COLUMN, SENTIMENT_CLASSES, RANDOM_STATE
)


# ── Seed for reproducibility (Probability) ───────────────────────
random.seed(RANDOM_STATE)
np.random.seed(RANDOM_STATE)


# ── Realistic text templates per sentiment ────────────────────────────────────
_POSITIVE_TEMPLATES = [
    "I absolutely love this {item}! It works perfectly and exceeded my expectations.",
    "Amazing {item}! Best purchase I have ever made. Highly recommend to everyone.",
    "This {item} is fantastic. The quality is outstanding and delivery was super fast.",
    "Great {item}! Very happy with my purchase. Will definitely buy again.",
    "Excellent {item}. It is exactly what I needed. Five stars without hesitation.",
    "Wonderful experience with this {item}. Customer service was also very helpful.",
    "The {item} is brilliant and well worth every penny. Totally satisfied!",
    "So glad I bought this {item}. It changed my daily routine for the better.",
    "Incredible {item}. The build quality and design are top notch. Love it!",
    "Perfect {item} for my needs. Setup was easy and it works flawlessly.",
    "I am thrilled with this {item}. It performs exactly as described.",
    "Outstanding {item}. Very impressed with the performance and durability.",
    "Best {item} on the market right now. Cannot recommend it enough!",
    "This {item} has made my life so much easier. Absolutely worth buying.",
    "Superb {item}! Arrived quickly and in perfect condition. Very happy.",
    "Loving this {item} every single day. It never lets me down.",
    "The {item} is a game changer! Far better than I expected.",
    "Really impressed with this {item}. Quality is exceptional for the price.",
    "This {item} is well designed and very intuitive to use. Great value!",
    "Awesome {item}! Works like a charm. Completely satisfied with my order.",
    "Just got this {item} and already love it. So easy to use.",
    "This product is simply the best! Would buy it again without hesitation.",
    "Highly satisfied with my purchase. The product arrived early and is perfect.",
    "The team was very supportive and the product quality is top tier.",
    "Exceptional quality and great price. This is exactly what I was looking for.",
    "Good {item}! Really good quality and great performance.",
    "Very good product. Works nicely and great design.",
    "Pretty good {item}. Very satisfied with this purchase.",
    "The {item} is not bad at all, actually quite good and pleasant!",
    "Not bad at all! Really pleased with this {item}.",
    "The {item} is not bad at all, works very well and great value.",
    "This {item} is not bad at all, good quality and very pleased.",
    "The phone is not bad at all, very good battery and smooth performance.",
    "So good! Best {item} I have purchased recently.",
    "Good experience overall. Great value for money.",
    "This {item} is good, works great.",
    "Very happy with this {item}. Works wonderfully and super fast.",
    "Great battery life and awesome display on this {item}.",
    "I really like this {item}. Excellent build and smooth performance.",
    "Satisfied with this purchase. Good quality and good value.",
    "Super happy with my purchase. Fast delivery and perfect condition.",
    "Loving this {item}. Best quality I have seen in a long time.",
]

_NEGATIVE_TEMPLATES = [
    "This {item} is bad. Really bad quality and poor design.",
    "Very bad experience with this {item}. Not recommended at all.",
    "Very bad product. Cheaply made and falls apart instantly.",
    "Such a bad {item}. Horrible performance and bad build quality.",
    "The {item} is bad, broke on the very first day.",
    "Bad purchase. Do not buy this {item}.",
    "Bad quality, totally disappointed with this {item}.",
    "The {item} is not good. Disappointed with the purchase.",
    "Not good at all. The {item} does not work properly.",
    "This {item} is not good, complete waste of money.",
    "I am not happy with this {item} at all. Very disappointed.",
    "Not satisfied with this {item}. Poor quality and poor service.",
    "The {item} is not working and definitely not worth the price.",
    "Dislike this {item}. Extremely bad performance and poor battery life.",
    "Poor battery life, poor build quality, very bad {item}.",
    "Not pleased with this purchase. Bad quality {item}.",
    "I am unhappy and dissatisfied with this {item}.",
    "The {item} is bad and slow. Do not recommend.",
    "Terrible battery life and bad display on this {item}.",
    "Worst experience ever. Horrible {item} and bad support.",
    "Worst {item} I have ever purchased. Broke after just two days of use.",
    "Very disappointed with this {item}. Quality is extremely poor and it does not work.",
    "Do not waste your money on this {item}. It stopped working almost immediately.",
    "Terrible experience. The {item} arrived broken and customer service was useless.",
    "This {item} is a scam. Nothing like the photos. Completely misleading listing.",
    "Horrible {item}. Stopped working after one week. Would give zero stars.",
    "This {item} is absolutely terrible. Complete waste of money. Do not buy.",
    "I regret buying this {item}. Total disappointment from packaging to performance.",
    "Awful {item}. Returned it immediately. The seller was unresponsive and rude.",
    "The {item} overheats constantly. Dangerous and completely unreliable.",
    "Never buying from this seller again. The {item} is garbage quality.",
    "Complete failure. The {item} does not work as advertised at all.",
    "Extremely disappointed. This {item} is far worse than the description suggests.",
    "The {item} is defective. Customer support refused to help with the return.",
    "Waste of time and money. The {item} broke within the first hour of use.",
    "This {item} is a disgrace. Poor quality control and terrible design.",
    "Misleading description. The {item} is nothing like what was shown in images.",
    "I am furious! The {item} arrived with missing parts and no instruction manual.",
    "Broken on arrival. Seller refused refund. This {item} is absolutely terrible.",
    "Would not recommend this {item} to anyone. Extremely frustrated with the purchase.",
    "The quality is appalling. This is clearly a counterfeit product.",
    "Very poor packaging and the product was damaged. Totally unacceptable.",
    "Useless product. Does not work at all. Seller is ignoring my messages.",
    "Strongly advise against buying this. The worst product I have seen in years.",
]

_NEUTRAL_TEMPLATES = [
    "The {item} is okay. Nothing special but it does what it is supposed to.",
    "Average {item}. It gets the job done but there are ordinary options available.",
    "The {item} arrived on time and works as described. Standard product.",
    "The {item} is fine. Meets basic everyday requirements.",
    "Okay product. The {item} functions normally.",
    "The {item} is satisfactory. Works as expected with standard performance.",
    "Reasonable {item}. Does the job adequately with standard features.",
    "Standard {item}. Works as described, ordinary quality.",
    "The {item} is acceptable. Average build quality and standard performance.",
    "Moderate quality {item}. It performs its basic function without issues.",
    "The {item} is just okay. Standard build quality and regular performance.",
    "Fairly standard {item}. Serves its purpose as described.",
    "It is an average product. The {item} works as expected.",
    "Normal {item} for this price range. Exactly as specified in the catalog.",
    "The {item} arrived in decent condition. Typical purchase.",
    "Passable {item}. Standard product with regular specifications.",
    "The {item} does what it says. Typical performance for this category.",
    "Acceptable product. Meets the basic specifications as listed.",
    "The experience was standard. Just a regular purchase.",
    "This {item} is functional. Regular model with basic capabilities.",
    "Typical product in this category. Basic design and normal operation.",
    "Received the {item} today. Packed normally and working as stated.",
    "The {item} operates according to the user manual.",
    "Standard delivery time and standard build quality for the {item}.",
]

_ITEMS = [
    "product", "phone", "laptop", "earphones", "camera", "watch", "tablet",
    "keyboard", "mouse", "charger", "bag", "shoes", "jacket", "book",
    "service", "app", "software", "delivery", "seller", "brand",
    "subscription", "experience", "setup", "feature", "design",
]

_SOCIAL_POSTS = {
    "Positive": [
        "Just tried the new update and it is actually amazing! #impressed",
        "Can't believe how good this turned out. So happy right now!",
        "Shoutout to the support team — they resolved my issue in minutes!",
        "This feature is exactly what I needed. Loving every bit of it!",
        "Best decision I made this year. Absolutely no regrets.",
        "The results are incredible. Far beyond what I had hoped for.",
        "Feeling grateful today. Things are going really well!",
        "This is genuinely life changing. Cannot stop telling people about it.",
        "Blown away by the customer experience. Truly world class service!",
        "Just finished and I am so proud of the outcome. Hard work pays off!",
        "Really good product! Very happy with how it turned out.",
        "The new update is actually not bad at all, quite impressed!",
        "So good! Works like a charm. Highly recommend.",
        "Good quality, good price, great customer service!",
    ],
    "Negative": [
        "This update ruined everything. Why do they keep breaking things?",
        "Absolutely terrible experience. Never using this service again.",
        "The app crashed and I lost all my data. Completely unacceptable!",
        "Still waiting for my refund after 3 weeks. This is a scam!",
        "Customer support is non-existent. Nobody responds to anything.",
        "Disappointed once again. They clearly don't care about users.",
        "Broken feature after update. This is getting ridiculous. #angry",
        "I want my money back! This product is not what was advertised at all.",
        "The worst app update in history. Everything worked fine before.",
        "Furious right now. Third time this issue has happened this month.",
        "Such a bad experience! Never ordering from here again.",
        "Very bad quality and worst delivery service ever.",
        "This is really not good. Super disappointed with the new version.",
        "Bad phone, bad battery, bad camera. Total waste of money.",
        "Not good at all. The app keeps failing every single time.",
    ],
    "Neutral": [
        "Got the new update. Some things changed. Will see how it goes.",
        "Tried the product. It is what it is. Standard experience.",
        "Received the delivery today. Regular package.",
        "The service is functional. Typical performance.",
        "The app does what it says. Average experience overall.",
        "Received my order today. Looks fine. Have not tested everything yet.",
        "It is okay I guess. Standard specifications.",
        "Used it for a week now. Typical standard results.",
        "The feature works as per the release notes.",
        "Standard update installed today. No issues observed.",
    ]
}


def _generate_dataset(n_samples: int = 6000, seed: int = RANDOM_STATE) -> pd.DataFrame:
    """
    Generate a realistic synthetic sentiment dataset.
    Uses seeded randomness for full reproducibility (Probability).

    Distribution: 40% Positive, 35% Negative, 25% Neutral
    (intentionally imbalanced to demonstrate class imbalance handling)
    """
    rng = np.random.default_rng(seed)
    records = []

    # Distribution ratios
    distribution = {
        "Positive": int(n_samples * 0.40),
        "Negative": int(n_samples * 0.35),
        "Neutral":  n_samples - int(n_samples * 0.40) - int(n_samples * 0.35),
    }

    # Base date for synthetic timestamps — last 365 days
    base_date = datetime(2025, 10, 31)

    template_map = {
        "Positive": _POSITIVE_TEMPLATES,
        "Negative": _NEGATIVE_TEMPLATES,
        "Neutral":  _NEUTRAL_TEMPLATES,
    }

    for sentiment, count in distribution.items():
        templates  = template_map[sentiment]
        social_pts = _SOCIAL_POSTS[sentiment]

        for i in range(count):
            # 30% social posts, 70% product reviews
            if rng.random() < 0.30:
                text = social_pts[int(rng.integers(0, len(social_pts)))]
            else:
                template = templates[int(rng.integers(0, len(templates)))]
                item     = _ITEMS[int(rng.integers(0, len(_ITEMS)))]
                text     = template.format(item=item)

            # Synthetic timestamp — weighted towards recent days
            days_ago = int(rng.integers(0, 365))
            ts = base_date - timedelta(days=int(days_ago))

            records.append({
                TEXT_COLUMN:      text,
                LABEL_COLUMN:     sentiment,
                TIMESTAMP_COLUMN: ts.strftime("%Y-%m-%d %H:%M:%S"),
                "source":         "synthetic",
            })

    df = pd.DataFrame(records)
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    return df


def load_dataset(force_regenerate: bool = False) -> pd.DataFrame:
    """
    Load the sentiment dataset.

    Priority:
      1. Existing raw CSV (already downloaded or generated)
      2. Generate synthetic dataset and save

    Args:
        force_regenerate: Regenerate even if CSV exists.

    Returns:
        pd.DataFrame with columns: text, sentiment, timestamp, source
    """
    if os.path.exists(RAW_CSV) and not force_regenerate:
        print(f"[DataLoader] Loading existing dataset: {RAW_CSV}")
        df = pd.read_csv(RAW_CSV)
        # Ensure required columns exist
        _validate_columns(df)
        return df

    print("[DataLoader] Generating synthetic dataset...")
    df = _generate_dataset(n_samples=6000)
    os.makedirs(os.path.dirname(RAW_CSV), exist_ok=True)
    df.to_csv(RAW_CSV, index=False)
    print(f"[DataLoader] Dataset saved -> {RAW_CSV}  ({len(df):,} records)")
    return df


def load_custom_csv(filepath: str, text_col: str, label_col: str = None) -> pd.DataFrame:
    """
    Load a user-supplied CSV file and map columns to standard names.

    Args:
        filepath:  Path to the CSV file.
        text_col:  Column containing the review/comment text.
        label_col: (Optional) Column containing sentiment labels.

    Returns:
        pd.DataFrame with standardised columns.
    """
    df = pd.read_csv(filepath)
    rename_map = {text_col: TEXT_COLUMN}
    if label_col and label_col != LABEL_COLUMN:
        rename_map[label_col] = LABEL_COLUMN
    df = df.rename(columns=rename_map)
    _validate_columns(df, require_label=(label_col is not None))
    return df


def _validate_columns(df: pd.DataFrame, require_label: bool = True):
    """Validate that expected columns are present."""
    if TEXT_COLUMN not in df.columns:
        raise ValueError(
            f"Column '{TEXT_COLUMN}' not found. "
            f"Available columns: {list(df.columns)}"
        )
    if require_label and LABEL_COLUMN not in df.columns:
        raise ValueError(
            f"Column '{LABEL_COLUMN}' not found. "
            f"Available columns: {list(df.columns)}"
        )


def get_dataset_profile(df: pd.DataFrame) -> dict:
    """
    Generate a comprehensive dataset profile dictionary.

    Data profiling as part of the Data Science Life Cycle.
    Missing value and duplicate analysis.

    Returns:
        dict with shape, dtypes, missing values, duplicates, class distribution.
    """
    profile = {
        "n_rows":       len(df),
        "n_cols":       len(df.columns),
        "columns":      list(df.columns),
        "dtypes":       df.dtypes.astype(str).to_dict(),
        "missing":      df.isnull().sum().to_dict(),
        "missing_pct":  (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
        "duplicates":   int(df.duplicated().sum()),
        "duplicate_pct":round(df.duplicated().sum() / len(df) * 100, 2),
        "memory_mb":    round(df.memory_usage(deep=True).sum() / 1e6, 3),
    }

    if LABEL_COLUMN in df.columns:
        vc = df[LABEL_COLUMN].value_counts()
        profile["class_distribution"] = vc.to_dict()
        profile["class_pct"]          = (vc / len(df) * 100).round(2).to_dict()
        profile["n_classes"]          = int(df[LABEL_COLUMN].nunique())

    if TEXT_COLUMN in df.columns:
        lengths = df[TEXT_COLUMN].dropna().str.split().str.len()
        profile["word_count_mean"] = round(float(lengths.mean()), 2)
        profile["word_count_std"]  = round(float(lengths.std()),  2)
        profile["word_count_min"]  = int(lengths.min())
        profile["word_count_max"]  = int(lengths.max())
        profile["word_count_median"] = float(lengths.median())

    return profile

