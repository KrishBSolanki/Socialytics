"""
src/database.py
===============
Module 11 – SQLite Database and Data Engineering

Implements:
  • Database schema initialisation
  • Insert / fetch / delete prediction records
  • Export to CSV
  • Prediction history analytics

Data Engineering, OLTP vs OLAP, Data Pipelines
  • OLTP: This SQLite database (insert, fetch individual records)
  • OLAP: The analytics dashboard (aggregate queries, trend analysis)
"""

import os
import sqlite3
from datetime import datetime
from typing import List, Optional

import pandas as pd

from src.config import DB_PATH, SENTIMENT_CLASSES


# ── Schema ────────────────────────────────────────────────────────────────────
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS predictions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_text            TEXT    NOT NULL,
    clean_text          TEXT,
    predicted_sentiment TEXT    NOT NULL,
    prob_positive       REAL,
    prob_negative       REAL,
    prob_neutral        REAL,
    confidence          REAL,
    source              TEXT    DEFAULT 'manual',
    created_at          TEXT    NOT NULL
);
"""

CREATE_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_sentiment  ON predictions (predicted_sentiment);
CREATE INDEX IF NOT EXISTS idx_created_at ON predictions (created_at);
"""


# ── Connection Helper ─────────────────────────────────────────────────────────
def _get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Return a SQLite connection with row_factory enabled."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# ── Initialise Database ───────────────────────────────────────────────────────
def init_db(db_path: str = DB_PATH):
    """
    Create the predictions table and indexes if they do not exist.
    Safe to call multiple times (idempotent).
    """
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.executescript(CREATE_TABLE_SQL + CREATE_INDEX_SQL)
    conn.commit()
    conn.close()
    print(f"[Database] Initialised -> {db_path}")


# ── Insert Prediction ─────────────────────────────────────────────────────────
def insert_prediction(
    raw_text:            str,
    predicted_sentiment: str,
    prob_positive:       float,
    prob_negative:       float,
    prob_neutral:        float,
    confidence:          float,
    clean_text:          str   = None,
    source:              str   = "manual",
    db_path:             str   = DB_PATH,
) -> int:
    """
    Insert a single prediction record into the database.

    OLTP operation — single transactional insert.

    Returns:
        The auto-generated row ID.
    """
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO predictions
          (raw_text, clean_text, predicted_sentiment,
           prob_positive, prob_negative, prob_neutral,
           confidence, source, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            raw_text, clean_text, predicted_sentiment,
            round(prob_positive, 4), round(prob_negative, 4), round(prob_neutral, 4),
            round(confidence, 4), source,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def insert_batch_predictions(predictions: List[dict], db_path: str = DB_PATH):
    """
    Bulk insert multiple predictions.

    Batch ETL process.

    Args:
        predictions: List of dicts with prediction fields.
    """
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = [
        (
            p.get("raw_text", ""),
            p.get("clean_text"),
            p.get("predicted_sentiment", ""),
            round(p.get("prob_positive", 0), 4),
            round(p.get("prob_negative", 0), 4),
            round(p.get("prob_neutral",  0), 4),
            round(p.get("confidence",    0), 4),
            p.get("source", "bulk_upload"),
            now,
        )
        for p in predictions
    ]
    cursor.executemany(
        """
        INSERT INTO predictions
          (raw_text, clean_text, predicted_sentiment,
           prob_positive, prob_negative, prob_neutral,
           confidence, source, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    conn.close()
    print(f"[Database] Inserted {len(rows)} batch predictions.")


# ── Fetch Records ─────────────────────────────────────────────────────────────
def fetch_all_predictions(db_path: str = DB_PATH) -> pd.DataFrame:
    """
    Retrieve all prediction records as a DataFrame.

    OLAP read — full table scan for analytics.
    """
    conn = _get_connection(db_path)
    df = pd.read_sql_query(
        "SELECT * FROM predictions ORDER BY created_at DESC", conn
    )
    conn.close()
    return df


def fetch_recent_predictions(n: int = 10, db_path: str = DB_PATH) -> pd.DataFrame:
    """Retrieve the most recent N predictions."""
    conn = _get_connection(db_path)
    df = pd.read_sql_query(
        "SELECT * FROM predictions ORDER BY created_at DESC LIMIT ?", conn, params=(n,)
    )
    conn.close()
    return df


def get_prediction_stats(db_path: str = DB_PATH) -> dict:
    """
    Compute aggregate statistics from stored predictions.

    OLAP aggregate query.
    """
    conn = _get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total = cursor.fetchone()[0]

    if total == 0:
        conn.close()
        return {"total": 0}

    stats = {"total": total}
    for sentiment in SENTIMENT_CLASSES:
        cursor.execute(
            "SELECT COUNT(*) FROM predictions WHERE predicted_sentiment = ?",
            (sentiment,)
        )
        count = cursor.fetchone()[0]
        stats[sentiment.lower()] = count
        stats[f"{sentiment.lower()}_pct"] = round(count / total * 100, 2)

    cursor.execute("SELECT AVG(confidence) FROM predictions")
    stats["avg_confidence"] = round(cursor.fetchone()[0] or 0, 4)

    conn.close()
    return stats


# ── Delete Records ────────────────────────────────────────────────────────────
def delete_all_predictions(db_path: str = DB_PATH) -> int:
    """
    Delete all prediction history.
    Returns the number of rows deleted.
    """
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    print(f"[Database] Deleted {deleted} prediction records.")
    return deleted


def delete_prediction_by_id(row_id: int, db_path: str = DB_PATH) -> bool:
    """Delete a single prediction by its ID. Returns True if deleted."""
    conn = _get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions WHERE id = ?", (row_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


# ── Export ────────────────────────────────────────────────────────────────────
def export_to_csv(output_path: str, db_path: str = DB_PATH) -> str:
    """Export all predictions to a CSV file."""
    df = fetch_all_predictions(db_path)
    df.to_csv(output_path, index=False)
    print(f"[Database] Exported {len(df)} records -> {output_path}")
    return output_path

