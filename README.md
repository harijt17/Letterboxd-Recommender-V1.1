# 🎬 Letterboxd Recommender

A personalized **content-based movie recommendation system** that analyzes a user's Letterboxd export and recommends movies based on their viewing history, ratings, reviews, and movie metadata.

Unlike collaborative filtering systems, this recommender builds a unique taste profile for every user using genres, directors, cast members, writers, keywords, languages, production countries, decades, and runtime preferences.

---

## ✨ Features

* 📦 Upload a Letterboxd export (`.zip`)
* 🎥 Automatic movie matching using title, year, and fuzzy matching
* ⭐ Personalized user profile built from ratings and watched history
* 🎯 Content-based recommendation engine
* 🧠 TF-IDF content similarity scoring
* 📊 Metadata-based recommendation scoring
* 🌈 Diversity filtering for varied recommendations
* ⚡ Optimized candidate generation using indexed lookups

---

# Recommendation Pipeline

```text
Letterboxd Export (.zip)
            │
            ▼
     Export Loader
            │
            ▼
      Movie Matcher
            │
            ▼
     User Profile Builder
            │
            ▼
   Candidate Generator
            │
            ▼
    Metadata Scoring
            │
            ▼
   Content Similarity
            │
            ▼
         Ranking
            │
            ▼
    Diversity Filter
            │
            ▼
 Recommended Movies
```

---

# Project Structure

```text
Letterboxd-Recommender-V1.1/

├── api/
├── benchmarks/
├── frontend/
├── matching/
├── preprocessing/
├── profiling/
├── recommendation/
├── uploads/

├── Data/
│   ├── raw/
│   └── processed/

├── download_dataset.py
├── requirements.txt
└── README.md
```

---

# Dataset

This project uses a processed movie metadata dataset generated from the **Ultimate 1 Million Movies Dataset (TMDB + IMDb)**.

The processed dataset is **not included** in this repository because it exceeds GitHub's file size limit.

Download it automatically by running:

```bash
python download_dataset.py
```

The dataset will be downloaded from Hugging Face and saved to:

```text
Data/processed/movies.parquet
```

---

# Installation

Clone the repository.

```bash
git clone https://github.com/harijt17/Letterboxd-Recommender-V1.1.git

cd Letterboxd-Recommender-V1.1
```

Install the required packages.

```bash
pip install -r requirements.txt
```

Download the processed dataset.

```bash
python download_dataset.py
```

---

# Running the Application

## Start the FastAPI Backend

```bash
uvicorn api.main:app --reload
```

## Start the Streamlit Frontend

```bash
streamlit run frontend/app.py
```

---

# How It Works

## 1. Export Loading

The application reads the uploaded Letterboxd export and extracts:

* Watched movies
* Ratings
* Reviews
* Watch dates
* Rewatch information
* Tags

---

## 2. Movie Matching

Each movie is matched against the processed movie dataset using:

* Exact title matching
* Release year validation
* RapidFuzz fuzzy matching

---

## 3. User Profile Generation

A personalized taste profile is created using:

* Genres
* Directors
* Cast
* Writers
* Keywords
* Production Countries
* Spoken Languages
* Decades
* Runtime

Movie ratings are used as weights to determine feature importance.

---

## 4. Candidate Generation

Potential recommendations are retrieved using indexed metadata lookups.

Already watched movies are automatically excluded.

---

## 5. Recommendation Scoring

Each candidate receives a score based on:

* Metadata similarity
* TF-IDF content similarity
* User preference weights

---

## 6. Ranking & Diversity

Movies are:

* Ranked by recommendation score
* Filtered for diversity
* Returned as personalized recommendations

---

# Technologies Used

## Backend

* Python
* FastAPI
* Pandas
* NumPy

## Recommendation Engine

* Content-Based Filtering
* TF-IDF
* RapidFuzz

## Frontend

* Streamlit

## Dataset

* TMDB
* IMDb

---

# Performance

Current performance using approximately **346,000 movies**:

| Stage                 | Approximate Time |
| --------------------- | ---------------: |
| Export Loading        |          ~0.15 s |
| Movie Matching        |          ~8–12 s |
| Profile Building      |          ~0.02 s |
| Candidate Generation  |             ~3 s |
| Recommendation Engine |             ~3 s |

---

# Future Improvements

* Faster movie matching
* Approximate nearest-neighbor search
* Hybrid recommendation system
* Explainable recommendations
* Docker support
* Cloud deployment
* Live Letterboxd profile import

---

# Author

**Hari Prasath JT**

GitHub: https://github.com/harijt17
