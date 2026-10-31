# Social Media Sentiment Analysis System

> **Academic DSC (Data Science & Computing) Capstone Project**  
> Technology: Python · Scikit-learn · NLTK · TF-IDF · Multinomial Naive Bayes · Streamlit · SQLite

---

## 📌 Project Overview

A complete, interactive machine learning application that classifies text reviews, feedback,
and social media comments into **Positive**, **Negative**, or **Neutral** sentiment using
NLP, TF-IDF feature extraction, and Multinomial Naive Bayes classification.

---

## 🧠 DSC Syllabus Coverage

| Unit | Topic | Status |
|------|-------|--------|
| 1 | Data Science Introduction & Life Cycle | ✅ |
| 2 | Big Data (5 V's) | ✅ Conceptual |
| 3 | Statistics, Probability, Bayes' Theorem | ✅ |
| 4 | Linear Algebra I — TF-IDF Matrix | ✅ |
| 5 | Linear Algebra II — SVD/LSA | ✅ Optional |
| 6 | Data Transformation & Integrity | ✅ |
| 7 | Optimization — GD, Hyperparameter Tuning | ✅ |
| 8 | Data Engineering — SQLite, OLTP/OLAP | ✅ |
| 9 | Time Series — Moving Avg, Smoothing | ✅ |
| 10 | Visualization & Capstone | ✅ |

---

## 🛠️ Technology Stack

- **Language**: Python 3.11+
- **ML / NLP**: Scikit-learn, NLTK, SciPy
- **Data**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn, WordCloud
- **App**: Streamlit
- **Database**: SQLite (built-in)
- **Model Storage**: Joblib

---

## 📁 Project Structure

```
social-sentiment-analysis/
│
├── app.py                    # Main Streamlit app (Overview page)
├── train_model.py            # Standalone model training script
├── requirements.txt
├── .gitignore
│
├── src/                      # Core Python modules
│   ├── config.py             # Global configuration
│   ├── data_loader.py        # Dataset loading + generation
│   ├── preprocessing.py      # NLP text cleaning pipeline
│   ├── eda.py                # Exploratory data analysis
│   ├── feature_extraction.py # TF-IDF + SVD
│   ├── train.py              # Model training + save/load
│   ├── evaluation.py         # Metrics computation
│   ├── prediction.py         # Single + batch prediction
│   ├── database.py           # SQLite operations
│   └── visualization.py      # Plotly chart helpers
│
├── pages/                    # Streamlit multi-page routing
│   ├── 1_Overview.py
│   ├── 2_Sentiment_Analyzer.py
│   ├── 3_Bulk_Analysis.py
│   ├── 4_Dataset_Explorer.py
│   ├── 5_Analytics.py
│   ├── 6_Model_Evaluation.py
│   ├── 7_Prediction_History.py
│   └── 8_About_Project.py
│
├── dataset/
│   ├── raw/                  # Raw dataset CSV
│   └── processed/            # Preprocessed dataset CSV
│
├── models/
│   ├── sentiment_model.pkl   # Trained pipeline (TF-IDF + NB)
│   └── model_metadata.json   # Training info + metrics
│
└── database/
    └── sentiment.db          # SQLite prediction history
```

---

## ⚡ Quick Start

### 1. Install Dependencies

```bash
# Windows
py -m pip install -r requirements.txt

# macOS / Linux
python3 -m pip install -r requirements.txt
```

### 2. Train the Model (Run Once)

```bash
py train_model.py
```

This will:
- Generate the sentiment dataset (6,000 records)
- Preprocess and clean the text
- Train TF-IDF + Multinomial Naive Bayes pipeline
- Save model to `models/sentiment_model.pkl`
- Print evaluation metrics
- Initialise the SQLite database

### 3. Launch the Application

```bash
py -m streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📊 Application Pages

| Page | Module | Description |
|------|--------|-------------|
| 🏠 Overview | — | KPI cards, module grid, system status |
| 💬 Sentiment Analyzer | 7 | Real-time single text analysis |
| 📂 Bulk Analysis | 8 | CSV upload + batch prediction |
| 🔍 Dataset Explorer | 1,2,3,4 | EDA, word clouds, preprocessing, TF-IDF |
| 📈 Analytics | 9,10 | Interactive dashboard + time series |
| 📊 Model Evaluation | 6 | Confusion matrix, metrics, NB vs LR |
| 🗄️ Prediction History | 11 | SQLite database browser + export |
| 📘 About Project | 12 | Abstract, math, viva Q&A, deployment |

---

## 🎯 Model Performance

*(After running `train_model.py` — actual results will vary)*

- **Algorithm**: Multinomial Naive Bayes
- **Features**: TF-IDF (unigrams + bigrams, 20,000 features)
- **Split**: 80% train / 20% test (stratified)
- **Evaluation**: Accuracy, Precision, Recall, F1-score, Confusion Matrix

---

## 📖 Academic Note

This project is developed for academic demonstration purposes.
The synthetic dataset is generated with controlled randomness (seed=42) for reproducibility.
All mathematical explanations, metric computations, and visualizations are implemented
using standard, peer-reviewed libraries and follow established DSC syllabus guidelines.

---

## 👨‍🎓 Academic Information

- **Subject**: Data Science and Computing (DSC)
- **Project Type**: Capstone / Final Project
- **Level**: Undergraduate

---

*Built with ❤️ for academic learning — not for production use without a real dataset.*
