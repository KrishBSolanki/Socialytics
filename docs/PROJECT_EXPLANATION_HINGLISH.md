# Complete Project Guide & Viva Preparation (English + Hinglish)
## Social Media Sentiment Analysis System — Data Science & Computing (DSC)

> **About this Document:**
> Ye document pure project ka complete, practical aur academic guide hai. Isme project ka **Folder Structure**, **End-to-End Pipeline**, **DSC Concepts/Units ka practical use**, aur **Viva Voce ke most important questions with detailed answers** shamil hain.
> Is document ko English + Hinglish mix format me likha gaya hai taaki viva, presentation aur code review ke waqt aap har ek concept ko bina kisi doubt ke confidence ke saath explain kar sakein!

---

## Table of Contents
1. [Project Overview (Aakhir ye project kya hai aur kya karta hai?)](#1-project-overview)
2. [Project Architecture & Complete Folder Structure](#2-project-architecture--complete-folder-structure)
3. [End-to-End Data Science Pipeline (Step-by-Step Breakdown)](#3-end-to-end-data-science-pipeline)
   - [Phase 1: Data Ingestion & Loading (`data_loader.py`)](#phase-1-data-ingestion--loading)
   - [Phase 2: Exploratory Data Analysis & Statistics (`eda.py`)](#phase-2-exploratory-data-analysis--statistics)
   - [Phase 3: Text Preprocessing & Negation Handling (`preprocessing.py`)](#phase-3-text-preprocessing--negation-handling)
   - [Phase 4: TF-IDF Vectorization & Vector Space (`feature_extraction.py`)](#phase-4-tf-idf-vectorization--vector-space)
   - [Phase 5: Model Training — Multinomial Naive Bayes (`train.py`)](#phase-5-model-training--multinomial-naive-bayes)
   - [Phase 6: Model Evaluation & Benchmarking (`evaluation.py`)](#phase-6-model-evaluation--benchmarking)
   - [Phase 7: Database & Prediction Auditing (`database.py`)](#phase-7-database--prediction-auditing)
   - [Phase 8: Time Series Trends & Visualizations (`visualization.py`)](#phase-8-time-series-trends--visualizations)
4. [DSC Syllabus & Academic Concept Mapping (Unit 1 to 10)](#4-dsc-syllabus--academic-concept-mapping)
5. [Key Technical Decisions & Architectural Highlights](#5-key-technical-decisions--architectural-highlights)
6. [Comprehensive Viva Voce Questions & Answers (Category-Wise)](#6-comprehensive-viva-voce-questions--answers)
   - [Category A: Fundamentals & NLP Basics](#category-a-fundamentals--nlp-basics)
   - [Category B: Mathematical & Statistical Formulations](#category-b-mathematical--statistical-formulations)
   - [Category C: ML Architecture & Code Implementation](#category-c-ml-architecture--code-implementation)
   - [Category D: Trap / Tricky Professor Questions](#category-d-trap--tricky-professor-questions)
   - [Category E: System Design, Database & Deployment](#category-e-system-design-database--deployment)

---

## 1. Project Overview

### What is this project? (Ye kya hai?)
**Social Media Sentiment Analysis System** ek production-grade, interactive web application hai jo social media posts, tweets, customer reviews aur comments ko read karke automatically detect karta hai ki unka sentiment kya hai:
- **Positive** (Khushi, appreciation, recommendation, good feedback)
- **Negative** (Gussa, complaint, disappointment, bad experience)
- **Neutral** (Factual news, normal enquiry, objective statement)

### Real-World Business Problem (Iska real world me kya use hai?)
Social media platforms (Twitter/X, Reddit, Instagram) aur E-commerce sites (Amazon, Flipkart) par daily millions of reviews aate hain. 
- Kisi human team ke liye possible nahi hai ki 1-1 review manually padhe.
- Simplistic keyword match (`"good"` = positive, `"bad"` = negative) fail ho jata hai kyunki agar koi likhe *"not good"*, toh traditional keyword search use galat positive classify kar deta hai!
- **Our Solution:** Hamara system advanced Natural Language Processing (NLP), custom negation preservation, TF-IDF n-gram vectorization aur Multinomial Naive Bayes probability model use karke accurate prediction karta hai within milliseconds.

---

## 2. Project Architecture & Complete Folder Structure

Project ka directory structure industry-standard clean architecture follow karta hai:

```
D:\Codebase\DSC_GP\
│
├── app.py                      # Main entrypoint; session state initialize aur Overview page par redirect karta hai
│
├── pages/                      # Multi-page Streamlit web app ke individual pages
│   ├── 1_Overview.py           # Dashboard overview, summary KPIs aur 12 interactive clickable module cards
│   ├── 2_Sentiment_Analyzer.py # Real-time single text review analyzer with confidence score & bar breakdown
│   ├── 3_Bulk_Analysis.py      # Batch CSV upload page — hazaro reviews ek saath analyze karke CSV export karo
│   ├── 4_Dataset_Explorer.py   # Dataset viewer, descriptive stats, class distribution, word clouds, SVD demo
│   ├── 5_Analytics.py          # Temporal analytics, 7-day rolling moving average, sentiment proportion charts
│   ├── 6_Model_Evaluation.py   # Confusion Matrix, Precision, Recall, Macro/Weighted F1, NB vs LR comparison
│   ├── 7_Prediction_History.py # SQLite database log viewer, filter by sentiment/date, CSV download, row deletion
│   └── 8_About_Project.py      # Abstract, 10 DSC modules implementation map, KaTeX formulas, Viva prep
│
├── src/                        # Core Data Science & ML Engine (Modular Python Scripts)
│   ├── __init__.py
│   ├── config.py               # Global parameters, paths, sentiment colors, random seed, stopwords
│   ├── icons.py                # Inline Lucide SVG generator (zero external CDN reliance, fast & clean)
│   ├── styles.py               # Custom Modern Dark Theme CSS, button states, card typography (Lato)
│   ├── data_loader.py          # Data ingestion, schema validation, synthetic generation fallback
│   ├── eda.py                  # Mean, variance, std dev, IQR, vocabulary size calculation
│   ├── preprocessing.py        # Text cleaning, lowercase, URL/HTML stripping, negation-preserving stopwords
│   ├── feature_extraction.py   # TF-IDF Vectorizer (unigrams + bigrams), document-term matrix, SVD
│   ├── train.py                # Pipeline construction, stratified split, MultinomialNB + LogisticRegression
│   ├── evaluation.py           # Classification report, Confusion matrix computation, macro/weighted F1
│   ├── prediction.py           # Live inference engine, confidence probability formatting
│   ├── database.py             # SQLite helper (ACID compliant): OLTP record insert, OLAP aggregations
│   └── visualization.py        # Plotly interactive graphs (distribution donut, line trend, confusion matrix)
│
├── dataset/                    # Training and demonstration data files
│   └── sentiment_dataset.csv   # Structured CSV (text, sentiment, timestamp, source)
│
├── models/                     # Serialized production machine learning artifacts
│   ├── sentiment_model.pkl     # Fitted scikit-learn Pipeline (TF-IDF + MultinomialNB) via joblib
│   └── model_metadata.json     # Hyperparameters, evaluation scores, vocabulary size, timestamp
│
├── database/                   # Persistent relational storage
│   └── sentiment.db            # SQLite database file storing manual & bulk prediction logs
│
├── docs/                       # Project documentation, academic reports & viva guides
│   ├── PROJECT_REPORT.md       # Full formal academic report for university submission
│   ├── VIVA_AND_DEMO_GUIDE.md  # Viva questions & quick teacher demo walkthrough
│   └── PROJECT_EXPLANATION_HINGLISH.md # (This File) Complete bilingual technical breakdown
│
├── notebooks/                  # Jupyter notebooks for interactive research & EDA experiments
│   └── exploratory_analysis.ipynb
│
├── pyrefly.toml                # Antigravity IDE Pyrefly type-checker configuration
├── pyproject.toml              # Project metadata & pyrefly tool settings
├── requirements.txt            # Python dependencies (streamlit, scikit-learn, nltk, plotly, etc.)
└── train_model.py              # Standalone CLI training script to retrain and persist models
```

---

## 3. End-to-End Data Science Pipeline

Hamara project ek classic **8-Phase Data Science Life Cycle** ko implement karta hai:

```
[Raw Text / CSV]
       │
       ▼
[Phase 1: Data Loader]  ──▶ Schema validation, missing values & duplicates handling
       │
       ▼
[Phase 2: EDA & Stats]  ──▶ Text length statistics (Mean, Std Dev, Variance), Class balance
       │
       ▼
[Phase 3: Preprocessing]──▶ Lowercase, Remove HTML/URLs, Tokenize, Keep Negations ("not", "never")
       │
       ▼
[Phase 4: TF-IDF Engine]──▶ Unigrams + Bigrams, Document-Term Matrix (Sparse Matrix)
       │
       ▼
[Phase 5: NB Classifier]──▶ Multinomial Naive Bayes + Laplace Smoothing (alpha=1.0)
       │
       ▼
[Phase 6: Evaluation]   ──▶ Confusion Matrix, Precision, Recall, Macro/Weighted F1, Accuracy
       │
       ▼
[Phase 7: Persistence]  ──▶ SQLite Database (OLTP inserts, OLAP aggregate analytics)
       │
       ▼
[Phase 8: Frontend UI]  ──▶ Streamlit Interactive Multi-Page Web App + Plotly Charts
```

---

### Phase 1: Data Ingestion & Loading (`src/data_loader.py`)
- **Kya karta hai?** Dataset ko disk se read karta hai (`sentiment_dataset.csv`).
- **Data Integrity Checks:**
  1. Missing values check karta hai (`df.dropna(subset=['text', 'sentiment'])`).
  2. Duplicate records remove karta hai.
  3. Text length validate karta hai (empty strings ko filter out karta hai).
- **Fallback Generation:** Agar CSV file exist na kare, toh seeded reproducible generator automatically 6,000+ realistic social media posts generate kar deta hai with timestamps taaki system kabhi crash na ho.

---

### Phase 2: Exploratory Data Analysis & Statistics (`src/eda.py`)
- **Descriptive Statistics:**
  - $\text{Mean Length } (\bar{x}) = \frac{1}{n}\sum x_i$ : Average review length in characters & words.
  - $\text{Variance } (\sigma^2) = \frac{1}{n}\sum (x_i - \bar{x})^2$ : Review lengths me kitna spread/deviation hai.
  - $\text{Standard Deviation } (\sigma) = \sqrt{\sigma^2}$ : Typical variation around the mean.
- **Class Balance & Imbalance Ratio:**
  - Sentiment classes ka count nikalta hai: $\text{Positive } (N_1), \text{Negative } (N_2), \text{Neutral } (N_3)$.
  - Imbalance Ratio: $r = \frac{\max(N_k)}{\min(N_k)}$. Agar $r \approx 1$, data balanced hai, jo model bias hone se bachata hai.

---

### Phase 3: Text Preprocessing & Negation Handling (`src/preprocessing.py`)
**Ye project ka sabse critical NLP component hai!**

#### The Step-by-Step Cleaning Flow:
1. **Lowercasing:** `"EXCELLENT"` $\rightarrow$ `"excellent"`.
2. **HTML & URL Removal:** Regex se `<p>`, `<br>`, `http://...` sab clean ho jate hain.
3. **Punctuation & Special Character Filtering:** Symbols `@, #, $, %, ^, *` remove kiye jate hain.
4. **Tokenization:** Text ko individual words ke list me split kiya jata hai using NLTK `word_tokenize`.
5. **Custom Stopword Removal (Negation Preservation):**
   - *Problem:* Standard NLTK stopword list me `"not"`, `"no"`, `"never"`, `"hardly"`, `"neither"` jaise words hote hain. Agar inko hata diya, toh `"The food is not good"` ban jayega `"food good"`, aur model Negative sentiment ko **Positive** predict kar dega!
   - *Our Solution:* Hamne ek custom `NEGATION_WORDS` set banaya hai. Preprocessing pipeline in polarity-shifters ko **kabhi delete nahi karta**.

---

### Phase 4: TF-IDF Vectorization & Vector Space (`src/feature_extraction.py`)
Machine learning algorithms string/text ko directly multiply nahi kar sakte. Hume text ko numbers (vectors) me badalna hota hai.

#### 1. Term Frequency (TF):
Document $d$ me word $t$ kitni baar aaya:
$$TF(t, d) = \frac{\text{Count of } t \text{ in } d}{\text{Total words in } d}$$

#### 2. Inverse Document Frequency (IDF):
Jo words har review me aate hain (jaise *"product"*, *"review"*), unka weight kam hona chahiye; aur jo rare informative words hain (jaise *"horrible"*, *"exceptional"*), unka weight high hona chahiye:
$$IDF(t) = \log\left(\frac{1 + N}{1 + df(t)}\right) + 1$$
*(Where $N$ = total documents, $df(t)$ = number of documents containing term $t$)*

#### 3. TF-IDF Score:
$$\text{TF-IDF}(t, d) = TF(t, d) \times IDF(t)$$

#### 4. N-Grams (Unigrams + Bigrams):
Hamara vectorizer `ngram_range=(1, 2)` use karta hai. Iska matlab single words (unigrams) ke saath saath do-do words ke pairs (bigrams) jaise `"not_bad"`, `"highly_recommend"`, `"poor_quality"` bhi as a single feature capture hote hain!

#### 5. Vector Space & Sparse Matrix:
Agar vocabulary me 10,000 words hain aur ek tweet me 15 words hain, toh 9,985 entries zero hongi! Memory bachane ke liye scikit-learn ise **CSR Sparse Matrix** me store karta hai (Linear Algebra concept).

---

### Phase 5: Model Training — Multinomial Naive Bayes (`src/train.py`)

#### Bayes' Theorem Formulation:
Given an input feature vector $\mathbf{x} = (x_1, x_2, \dots, x_n)$, probability of class $C_k \in \{\text{Pos}, \text{Neg}, \text{Neu}\}$:
$$P(C_k \mid \mathbf{x}) = \frac{P(C_k) \cdot P(\mathbf{x} \mid C_k)}{P(\mathbf{x})}$$

#### Naive Independence Assumption:
Naive Bayes assume karta hai ki sentence ke saare words ek dusre se conditionally independent hain:
$$P(\mathbf{x} \mid C_k) = \prod_{i=1}^n P(x_i \mid C_k)$$

#### Laplace (Add-1) Smoothing:
Agar koi test sentence me aisa word aa gaya jo training ke dauran class $C_k$ me kabhi nahi dekha gaya tha, toh $P(w \mid C_k) = 0$ ho jayega. Pure multiplication ki wajah se entire probability 0 ho jayegi!
Is **Zero-Probability Problem** ko solve karne ke liye Laplace Smoothing ($\alpha = 1.0$) use hoti hai:
$$P(w_i \mid C_k) = \frac{\text{count}(w_i, C_k) + \alpha}{\sum_w \text{count}(w, C_k) + \alpha \cdot |V|}$$

#### scikit-learn Pipeline (Data Leakage Avoidance):
```python
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
    ('nb', MultinomialNB(alpha=1.0))
])
pipeline.fit(X_train, y_train)
```
*Why Pipeline?* Agar pehle pure dataset par TF-IDF fit karte aur baad me train/test split karte, toh test set ke words training vocabulary me leak ho jate (Data Leakage)! Pipeline ensure karta hai ki vectorizer sirf aur sirf `X_train` par fit hota hai.

---

### Phase 6: Model Evaluation & Benchmarking (`src/evaluation.py`)

Hume sirf simple accuracy par rely nahi karna chahiye, especially multi-class classification me.

| Metric | Formula | Practical Meaning |
|---|---|---|
| **Accuracy** | $\frac{TP + TN}{\text{Total}}$ | Overall kitne percent predictions sahi the. |
| **Precision** | $\frac{TP}{TP + FP}$ | Jab model ne "Positive" bola, toh unme se sach me kitne positive the? (Low false alarms) |
| **Recall** | $\frac{TP}{TP + FN}$ | Dataset ke saare actual positives me se model kitno ko dhoond paya? |
| **F1-Score** | $2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$ | Precision aur Recall ka harmonic mean (Balanced Score). |
| **Macro F1** | $\frac{F1_{\text{pos}} + F1_{\text{neg}} + F1_{\text{neu}}}{3}$ | Har class ko equal weight deta hai (chahe class chhoti ho ya badi). |
| **Weighted F1**| $\sum \frac{N_c}{N} F1_c$ | Class ke size ke hisab se weighted average nikalta hai. |

---

### Phase 7: Database & Prediction Auditing (`src/database.py`)
Project me embedded **SQLite** database (`database/sentiment.db`) use kiya gaya hai:
- **Table Schema:** `predictions` table contains `id`, `timestamp`, `raw_text`, `clean_text`, `predicted_sentiment`, `prob_positive`, `prob_negative`, `prob_neutral`, `confidence`, `source`.
- **OLTP (Online Transaction Processing):** Jab user Single Analyzer me review enter karta hai ya Bulk CSV upload karta hai, row-by-row instant transactional write hoti hai (`INSERT INTO predictions...`).
- **OLAP (Online Analytical Processing):** Jab Analytics Dashboard ya History page load hota hai, database aggregate analytical queries run karta hai (`COUNT(*)`, `GROUP BY predicted_sentiment`, date-filtering).

---

### Phase 8: Time Series Trends & Visualizations (`src/visualization.py`)
- **Daily Volume & Proportion:** Daily sentiments ko aggregate karke stacked bar / line charts generate kiye jate hain.
- **7-Day Rolling Moving Average:**
  Daily sentiment me daily noise aur random fluctuations hote hain. 7-day moving average curve ko smooth banata hai taaki long-term sentiment trajectory (brand health) clear dikhai de:
  $$MA_t = \frac{1}{7}\sum_{i=0}^{6} y_{t-i}$$

---

## 4. DSC Syllabus & Academic Concept Mapping

Viva me agar examiner pooche: *"Aapne apne course curriculum ke kaun-kaun se units is project me implement kiye hain?"*, toh ye table unke samne rakhna:

| DSC Unit / Concept | Syllabus Topic | Practical Implementation in Project | Code Location |
|:---:|:---|:---|:---|
| **Unit 1** | **Introduction to Data Science** | Data Science Life Cycle ke saare 8 phases step-by-step implement kiye gaye hain. | `app.py`, `src/data_loader.py` |
| **Unit 2** | **Big Data Concepts (5 Vs)** | Volume (batch processing), Velocity (sub-second live inference), Variety (text, CSV, JSON metadata), Veracity (noise cleaning). | `pages/8_About_Project.py`, `src/data_loader.py` |
| **Unit 3** | **Statistics & Probability** | Mean, Variance, Std Dev of text lengths; Bayes' Theorem formulation; Laplace probability smoothing. | `src/eda.py`, `src/train.py`, `pages/4_Dataset_Explorer.py` |
| **Unit 4** | **Linear Algebra I** | Document-Term Matrix (DTM); TF-IDF vector space; Vector normalization ($L_2$ norm). | `src/feature_extraction.py` |
| **Unit 5** | **Linear Algebra II** | High-dimensional sparse matrix representations; TruncatedSVD (Singular Value Decomposition) for dimensionality reduction / LSA. | `src/feature_extraction.py` (`perform_svd_analysis`) |
| **Unit 6** | **Data Transformation & Integrity** | Text normalization, tokenization, negation-preserving stopword filtering, stratified splitting without data leakage. | `src/preprocessing.py`, `src/train.py` |
| **Unit 7** | **Optimization in ML** | Contrast between closed-form MLE (Naive Bayes) vs Gradient-based Loss Optimization (Logistic Regression via L-BFGS). | `src/train.py` (`train_logistic_regression`), `pages/6_Model_Evaluation.py` |
| **Unit 8** | **Data Engineering & Databases** | Relational ACID-compliant SQLite storage; OLTP real-time prediction logs vs OLAP analytical KPI aggregations. | `src/database.py`, `pages/7_Prediction_History.py` |
| **Unit 9** | **Time Series Analysis** | Temporal chronological sorting, daily sentiment ratios, 7-day rolling moving average smoothing, trend detection. | `pages/5_Analytics.py`, `src/visualization.py` |
| **Unit 10** | **Data Visualization & Deployment** | Multi-page Streamlit web architecture, Plotly interactive charts, confusion matrix heatmaps, Joblib model serialization. | `app.py`, `pages/*.py`, `models/sentiment_model.pkl` |

---

## 5. Key Technical Decisions & Architectural Highlights

### 1. Why Multinomial Naive Bayes instead of Deep Learning / BERT?
- **Viva Answer:** 
  *"Sir, BERT ya LLM model bahut compute-heavy aur slow hote hain (high latency, requires expensive GPUs). Production environment me jahan thousands of incoming tweets ko real-time analyze karna ho, Multinomial Naive Bayes provides sub-5ms inference latency with exceptionally low memory footprint, while maintaining high accuracy (~85-90%) on TF-IDF unigram+bigram representations."*

### 2. Why Negation Preservation is Critical?
- **Viva Answer:**
  *"Traditional NLP stopwords filter out words like 'not', 'never', 'no'. Lekin sentiment analysis me ye valence-shifters hote hain. Agar 'not' delete ho gaya, toh 'not happy' ban jayega 'happy'—aur model negative statement ko positive predict karega. Hamara custom pipeline specifically negation words ko preserve karta hai."*

### 3. Why Scikit-Learn Pipeline?
- **Viva Answer:**
  *"Pipeline prevents Data Leakage. Agar hum split se pehle vectorizer fit karte, toh test set ke terms aur frequencies training data me leak ho jate, jisse evaluation score artificially inflate ho jata. Pipeline guarantees that the vectorizer only fits on `X_train`."*

### 4. Why Streamlit with `@st.cache_resource`?
- **Viva Answer:**
  *"Model bar-bar disk se load nahi hona chahiye har click par. `@st.cache_resource` model pipeline ko RAM me singleton pattern ki tarah ek hi baar load karta hai, jisse har page navigation fast aur seamless rehta hai."*

---

## 6. Comprehensive Viva Voce Questions & Answers

### Category A: Fundamentals & NLP Basics

#### Q1: What is Sentiment Analysis?
> **Answer (English):** Sentiment analysis (also known as opinion mining) is a natural language processing technique used to determine whether textual data carries a positive, negative, or neutral emotional tone.
> 
> **Hinglish Explanation:** Sentiment analysis ka simple matlab hai computer ko ye sikhana ki likhe huye text ka emotional mood ya opinion kya hai—kya user khush hai (Positive), gusse me ya pareshan hai (Negative), ya fir sirf facts share kar raha hai (Neutral).

#### Q2: What are the main steps in text preprocessing?
> **Answer (English):**
> 1. Case normalization (lowercasing)
> 2. Noise removal (removing HTML tags, URLs, and special characters)
> 3. Tokenization (splitting sentence into individual words/tokens)
> 4. Stopword filtering with negation preservation
> 
> **Hinglish Explanation:** Sabse pehle text ko lowercase karte hain taaki "Good" aur "good" alag alag na maane jayein. Fir HTML tags aur symbols hatate hain. Phir sentence ko words me todte hain (tokenization). Aur aakhri me useless words (stopwords) hatate hain lekin "not" aur "never" ko rakhte hain.

#### Q3: What is the difference between Unigrams and Bigrams?
> **Answer (English):** A unigram is a single continuous token (e.g., `"good"`), while a bigram is a contiguous sequence of two words (e.g., `"not good"`, `"very fast"`). 
> 
> **Hinglish Explanation:** Unigram matlab 1 akela word. Bigram matlab do words ka pair. Bigrams sentiment analysis ke liye bahut zaroori hain kyunki `"not"` aur `"good"` alag alag unigram ho sakte hain, lekin jab vo milkar `"not good"` bigram bante hain tabhi asli negative meaning samajh aati hai.

---

### Category B: Mathematical & Statistical Formulations

#### Q4: Explain Bayes' Theorem and how Naive Bayes uses it.
> **Answer (English):** Bayes' theorem calculates the posterior probability of a class $C_k$ given feature vector $\mathbf{x}$:
> $$P(C_k \mid \mathbf{x}) = \frac{P(C_k) \cdot P(\mathbf{x} \mid C_k)}{P(\mathbf{x})}$$
> The classifier chooses the class that maximizes this posterior probability:
> $$\hat{y} = \arg\max_{k} P(C_k) \prod_{i=1}^n P(x_i \mid C_k)$$
> 
> **Hinglish Explanation:** Bayes' Theorem hume batata hai ki kisi text ke aane par uske Positive, Negative ya Neutral hone ki kitni sambhavna (probability) hai. Naive Bayes assume karta hai ki har word akele kaam karta hai, isliye hum har word ki individual conditional probability ko multiply kar dete hain.

#### Q5: What is Laplace Smoothing and why is $\alpha=1$ used?
> **Answer (English):** Laplace smoothing prevents zero probabilities for unseen words in the test set. Without smoothing, if $P(w_i \mid C_k) = 0$, the entire product collapses to 0. Laplace smoothing adds $\alpha=1$ to the numerator and $\alpha \cdot |V|$ to the denominator:
> $$P(w_i \mid C_k) = \frac{\text{count}(w_i, C_k) + 1}{\sum_w \text{count}(w, C_k) + |V|}$$
> 
> **Hinglish Explanation:** Agar test set me koi naya word aa gaya jo training me nahi tha, toh uski probability 0 ho jayegi. Multiplication ki wajah se pure sentence ki probability 0 ban jayegi! Laplace smoothing numerator me 1 aur denominator me vocabulary size add karke har word ko ek chhota sa positive number deta hai taaki formula kabhi zero na bane.

#### Q6: How does TF-IDF differ from simple Word Count (Bag of Words)?
> **Answer (English):** Bag of Words counts simple raw frequencies, which gives undue importance to frequently repeating common words. TF-IDF balances Term Frequency (TF) with Inverse Document Frequency (IDF), discounting words that appear across all documents and amplifying words that are distinctive to a specific document.
> 
> **Hinglish Explanation:** Bag of Words sirf ginta hai ki word kitni baar aaya. Agar "phone" 50 baar aaya toh BoW use sabse bada number dega. Lekin TF-IDF ye dekhta hai ki agar "phone" har document me hai toh vo common word hai, uska weight ghata do; aur agar "fantastic" sirf specific positive review me hai toh use high weight do.

---

### Category C: ML Architecture & Code Implementation

#### Q7: Why Multinomial Naive Bayes instead of Gaussian Naive Bayes?
> **Answer (English):** Gaussian Naive Bayes assumes features are continuous and normally distributed (bell-shaped curve). Text TF-IDF and count matrices are discrete, non-negative, and heavily sparse (most entries are 0). Multinomial Naive Bayes models discrete multinomial distributions, which matches text frequency vectors.
> 
> **Hinglish Explanation:** Gaussian NB assume karta hai ki data continuous normal distribution me hai (jaise height ya weight). Lekin text data sparse aur non-negative hota hai (words ya toh hote hain ya 0 hote hain). Isliye text ke liye hamesha Multinomial Naive Bayes use hota hai.

#### Q8: What is Data Leakage and how did you prevent it?
> **Answer (English):** Data leakage occurs when test data characteristics inadvertently contaminate the training phase. If `TfidfVectorizer.fit_transform()` is executed on the whole dataset before splitting, the test set vocabulary and IDF calculations leak into training. We prevent this by wrapping vectorizer and classifier in an `sklearn.pipeline.Pipeline`, fitting strictly on `X_train`.
> 
> **Hinglish Explanation:** Agar hum train/test split karne se pehle pure dataset par TF-IDF fit karte, toh test set ke secret words model ko pehle se pata chal jate! Ise Data Leakage kehte hain. Hamne Scikit-Learn ka `Pipeline` use kiya jo strictly training set par fit hota hai aur test set ko as unseen data transform karta hai.

#### Q9: What is the difference between Macro F1 and Weighted F1?
> **Answer (English):**
> - **Macro F1:** Unweighted mean of F1 scores across classes: $\frac{F1_{\text{pos}} + F1_{\text{neg}} + F1_{\text{neu}}}{3}$. Gives equal importance to all classes regardless of sample size.
> - **Weighted F1:** Averages F1 scores weighted by the number of true instances in each class.
> 
> **Hinglish Explanation:** Macro F1 har class ko barabar treat karta hai (chahe kisi class ke sirf 100 samples ho aur dusri ke 5000). Weighted F1 class ke sample size ke hisaab se weight deta hai. Imbalanced dataset me Macro F1 model ki asli quality check karne ke liye better hota hai.

---

### Category D: Trap / Tricky Professor Questions

#### Q10: "Did your Naive Bayes model use Gradient Descent during training?" (Trap Question!)
> **Answer (English):** No, Multinomial Naive Bayes does **not** use Gradient Descent. It has a closed-form analytic solution computed directly using Maximum Likelihood Estimation (counting frequencies and dividing). However, to demonstrate optimization concepts (DSC Unit 7), we trained a comparative **Logistic Regression** model, which uses gradient-based loss minimization (L-BFGS).
> 
> **Hinglish Explanation:** Examiner ko turant bolna: *"Nahi sir! Naive Bayes me Gradient Descent nahi hota."* Naive Bayes direct counting aur probability formula (Closed-Form Solution) se train hota hai. Gradient Descent hamare project me **Logistic Regression** comparative model me use hua hai jahan cross-entropy loss minimize hoti hai.

#### Q11: "What happens if a user enters: 'The phone is not bad at all'?"
> **Answer (English):** Because of bigram extraction (`ngram_range=(1, 2)`) and our custom negation-preserving stopwords filter, the token `"not bad"` is preserved as a single feature with positive sentiment orientation, preventing it from being classified as negative.
> 
> **Hinglish Explanation:** Traditional model ise "bad" dekh kar negative bol deta. Lekin hamara preprocessing pipeline "not" ko delete nahi karta aur TF-IDF bigram `"not bad"` ko ek saath capture karta hai, jisse model ise accurate positive/neutral sentiment me classify karta hai.

#### Q12: "Why is Accuracy alone misleading for classification?"
> **Answer (English):** If a dataset has 90% positive reviews and 10% negative reviews, a dumb classifier predicting "Positive" for everything achieves 90% accuracy, yet it is completely unable to detect negative complaints. F1-score and Confusion Matrix reveal this flaw.
> 
> **Hinglish Explanation:** Agar 100 reviews me se 90 positive hain aur 10 negative hain, aur model bina soche sabko "Positive" bol de, tab bhi uski accuracy 90% aayegi! Lekin model negative identify karne me 0% hai. Isliye Precision, Recall aur Confusion Matrix dekhna zaroori hai.

---

### Category E: System Design, Database & Deployment

#### Q13: How are OLTP and OLAP demonstrated in your SQLite database?
> **Answer (English):**
> - **OLTP (Online Transaction Processing):** Demonstrated during live manual and bulk predictions via fast, single-row/batch ACID-compliant SQL inserts (`INSERT INTO predictions`).
> - **OLAP (Online Analytical Processing):** Demonstrated on Analytics and History pages via analytical SQL aggregations (`COUNT`, `GROUP BY predicted_sentiment`, temporal range filtering).
> 
> **Hinglish Explanation:**
> - OLTP ka matlab transactional entry: Jaise hi user ne review type karke "Save" dabaya, turant 1 record database me insert ho gaya.
> - OLAP ka matlab analytical summary: Analytics dashboard par hum `GROUP BY sentiment` aur aggregate queries chala kar charts aur KPIs render karte hain.

#### Q14: Why do you calculate a 7-Day Moving Average in time series analysis?
> **Answer (English):** Daily sentiment data exhibits high day-to-day variance and noise. A 7-day rolling moving average smooths high-frequency noise and highlights the underlying medium-to-long term sentiment trajectory.
> 
> **Hinglish Explanation:** Daily reviews me Monday ko zyada complaints ho sakti hain aur Sunday ko kam. Is daily up-down noise ko smooth karne ke liye 7-day moving average use karte hain taaki overall brand reputation ka trend clearly dikhe.

#### Q15: How does the application prevent retraining on every page refresh?
> **Answer (English):** The trained model is serialized to disk using `joblib` as `models/sentiment_model.pkl`. In Streamlit, it is loaded once into memory using `@st.cache_resource`, ensuring sub-second page rendering without repeated retraining.
> 
> **Hinglish Explanation:** Model ko train karke `.pkl` file me save kiya gaya hai. Streamlit me `@st.cache_resource` decorator use kiya hai jo model ko memory me cache rakhta hai. Isliye jab bhi user tab badalta hai, model dubara retrain ya reload nahi hota.

---

## 7. Quick 2-Minute Demo Script (For Project Presentation)

Agar viva me teacher bole: *"2 minute me apna project demo karke dikhao"*, toh ye steps follow karein:

1. **Step 1: Overview Page (`1_Overview.py`)**
   - App open karein (`http://localhost:8501`).
   - Teacher ko batayein: *"Sir, ye dashboard hamara Social Media Sentiment Analysis system hai jo modular architecture par built hai. Isme total 12 modules hain."*
2. **Step 2: Sentiment Analyzer (`2_Sentiment_Analyzer.py`)**
   - Quick example button click karein ya type karein: *"The battery life is not good, totally disappointed."*
   - Click **Analyze Sentiment**.
   - Show karein: Prediction = **Negative (Confidence: 94%)**, saath me probability breakdown bar chart dikhayein.
   - Point out karein: *"Sir, dekhiye 'not good' me negation preserve hua hai isliye model ne accurate negative detect kiya."*
3. **Step 3: Model Evaluation (`6_Model_Evaluation.py`)**
   - Confusion Matrix Heatmap aur Macro F1 score dikhayein.
   - Mention karein: *"Sir, humne Naive Bayes ko Logistic Regression ke saath compare kiya hai optimization showcase karne ke liye."*
4. **Step 4: Analytics Dashboard (`5_Analytics.py`)**
   - 7-Day Moving Average trend chart dikhayein.
   - Mention karein: *"Ye Time Series Analysis hai jo daily sentiment trend ko smooth karke dikhata hai."*
5. **Step 5: Prediction History (`7_Prediction_History.py`)**
   - SQLite database table dikhayein aur CSV export button showcase karein.
   - Mention karein: *"Har prediction SQLite database me OLTP pattern me log hoti hai aur yahan se OLAP analytics ke liye query hoti hai."*

---

*End of Guide — All the best for your Project Presentation & Viva!*

