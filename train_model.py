"""
train_model.py
==============
Standalone training script.

Run this ONCE to train and save the model:
  python train_model.py

This must be executed before launching the Streamlit app.

Phase 2–6: Dataset loading → Preprocessing → TF-IDF → Training → Evaluation → Save
"""

import json
import sys
import os

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import pandas as pd

# ── Path fix for running from project root ────────────────────────────────────
sys.path.insert(0, ".")

from src.config import (
    MODEL_PATH, METADATA_PATH, PROCESSED_CSV,
    TEXT_COLUMN, LABEL_COLUMN, SENTIMENT_CLASSES
)
from src.data_loader import load_dataset, get_dataset_profile
from src.preprocessing import preprocess_dataframe, get_preprocessing_stats
from src.train import (
    build_nb_pipeline, build_lr_pipeline,
    split_data, train_model, cross_validate_model,
    save_model, load_metadata
)
from src.evaluation import compute_metrics
from src.database import init_db


def run_training():
    print("=" * 60)
    print("  SOCIAL MEDIA SENTIMENT ANALYSIS — MODEL TRAINING")
    print("=" * 60)

    # ── Step 1: Load Dataset ──────────────────────────────────────────────
    print("\n[1/6] Loading dataset...")
    df_raw = load_dataset(force_regenerate=True)
    profile = get_dataset_profile(df_raw)
    print(f"      Records  : {profile['n_rows']:,}")
    print(f"      Columns  : {profile['columns']}")
    print(f"      Missing  : {profile['missing']}")
    print(f"      Duplicates: {profile['duplicates']}")
    if "class_distribution" in profile:
        print(f"      Classes  : {profile['class_distribution']}")

    # ── Step 2: Preprocess ────────────────────────────────────────────────
    print("\n[2/6] Preprocessing text...")
    df_clean = preprocess_dataframe(df_raw)
    pre_stats = get_preprocessing_stats(df_raw, df_clean)
    print(f"      Rows removed  : {pre_stats['records_removed']}")
    print(f"      Vocab (raw)   : {pre_stats['vocab_raw']:,}")
    print(f"      Vocab (clean) : {pre_stats['vocab_clean']:,}")

    # Save processed dataset
    import os
    os.makedirs(os.path.dirname(PROCESSED_CSV), exist_ok=True)
    df_clean.to_csv(PROCESSED_CSV, index=False)
    print(f"      Saved -> {PROCESSED_CSV}")

    # ── Step 3: Train/Test Split ──────────────────────────────────────────
    print("\n[3/6] Splitting data (80/20 stratified)...")
    X_train, X_test, y_train, y_test = split_data(df_clean)

    # ── Step 4: Train Naive Bayes ─────────────────────────────────────────
    print("\n[4/6] Training Multinomial Naive Bayes pipeline...")
    nb_pipeline = train_model(X_train, y_train, model_type="naive_bayes")

    # ── Step 5: Evaluate ──────────────────────────────────────────────────
    print("\n[5/6] Evaluating model...")
    y_pred   = nb_pipeline.predict(X_test)
    nb_metrics = compute_metrics(y_test, y_pred, labels=SENTIMENT_CLASSES)

    print(f"\n  +--------------------------------------+")
    print(f"  |  Naive Bayes Results                 |")
    print(f"  +--------------------------------------+")
    print(f"  |  Accuracy       : {nb_metrics['accuracy']:.4f}             |")
    print(f"  |  F1 (Macro)     : {nb_metrics['f1_macro']:.4f}             |")
    print(f"  |  F1 (Weighted)  : {nb_metrics['f1_weighted']:.4f}             |")
    print(f"  |  Precision(Mac) : {nb_metrics['precision_macro']:.4f}             |")
    print(f"  |  Recall (Mac)   : {nb_metrics['recall_macro']:.4f}             |")
    print(f"  +--------------------------------------+")

    # Optional: Logistic Regression comparison
    print("\n  [Optional] Training Logistic Regression for comparison...")
    try:
        lr_pipeline = train_model(X_train, y_train, model_type="logistic_regression")
        y_pred_lr   = lr_pipeline.predict(X_test)
        lr_metrics  = compute_metrics(y_test, y_pred_lr, labels=SENTIMENT_CLASSES)
        print(f"  LR Accuracy: {lr_metrics['accuracy']:.4f} | F1 Macro: {lr_metrics['f1_macro']:.4f}")
    except Exception as e:
        print(f"  LR training skipped: {e}")
        lr_metrics = {}

    # ── Step 6: Save ──────────────────────────────────────────────────────
    print("\n[6/6] Saving model and metadata...")

    metadata = {
        "model_type":        "MultinomialNB",
        "pipeline_steps":    ["TfidfVectorizer", "MultinomialNB"],
        "training_samples":  len(X_train),
        "test_samples":      len(X_test),
        "classes":           SENTIMENT_CLASSES,
        "nb_metrics":        nb_metrics,
        "lr_metrics":        lr_metrics,
        "preprocessing": {
            "records_removed": pre_stats["records_removed"],
            "vocab_clean":     pre_stats["vocab_clean"],
        },
        "dataset_profile":   {
            "n_rows":              profile["n_rows"],
            "class_distribution":  profile.get("class_distribution", {}),
        },
    }

    save_model(nb_pipeline, metadata)

    # ── Initialise Database ───────────────────────────────────────────────
    init_db()

    print("\n[SUCCESS] Training complete! You can now launch the app:")
    print("   streamlit run app.py\n")


if __name__ == "__main__":
    run_training()
