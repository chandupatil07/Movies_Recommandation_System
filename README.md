# 🎬 Movie Recommendation System

A content-based movie recommendation system that suggests similar movies based on user selection using NLP and cosine similarity.

---

## 📌 Project Overview

This project recommends movies by analyzing movie content such as:
- Overview
- Genres
- Keywords
- Cast

It uses Natural Language Processing (NLP) techniques to find similarity between movies.

---

## 📂 Dataset

- TMDB 5000 Movies Dataset
- Files used:
  - tmdb_5000_movies.csv
  - tmdb_5000_credits.csv

---

## ⚙️ Technologies Used

- Python
- Pandas, NumPy
- Scikit-learn
- NLTK
- Streamlit (for UI)
- Jupyter Notebook

---

## 🧠 How It Works

1. Load and merge movie & credits datasets
2. Clean and preprocess data
3. Combine important features into a single `tags` column
4. Convert text into vectors using CountVectorizer
5. Calculate cosine similarity between movies
6. Recommend top 5 similar movies

---

## 🚀 How to Run the Project

```bash
pip install -r requirements.txt
streamlit run app/app.py
