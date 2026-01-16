import streamlit as st
import pickle
import pandas as pd
import requests
import time
import gdown
import os

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# ---------------------- CUSTOM CSS ----------------------
st.markdown("""
    <style>
    .stApp {
        background: url("https://www.transparenttextures.com/patterns/cubes.png"),
        linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-size: cover;
        color: white;
        font-family: 'Poppins', sans-serif;
    }

    h1 {
        text-align: center;
        color: #ffcc00;
        font-size: 3rem;
        text-shadow: 3px 3px 8px #000000;
    }

    h3 {
        text-align: center;
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 400;
    }

    .movie-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        transition: 0.3s;
        backdrop-filter: blur(6px);
    }

    .movie-card:hover {
        transform: scale(1.08);
        background: rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
    }

    .movie-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #ffcc00;
        margin-top: 10px;
    }

    .movie-info {
        font-size: 0.9rem;
        color: #ddd;
    }

    .stButton button {
        background-color: #ff4757;
        color: white;
        border-radius: 10px;
        padding: 10px 25px;
        font-size: 1rem;
        border: none;
    }

    .stButton button:hover {
        background-color: #e84118;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- LOAD SIMILARITY (GOOGLE DRIVE) ----------------------
SIM_URL = "https://drive.google.com/uc?id=1IOmttRuwby4Awf4X1yLxZBzMvZd5tV51"
SIM_PATH = "similarity.pkl"

@st.cache_resource
def load_similarity():
    if not os.path.exists(SIM_PATH):
        with st.spinner("Loading recommendation engine..."):
            gdown.download(SIM_URL, SIM_PATH, quiet=False)
    with open(SIM_PATH, "rb") as f:
        return pickle.load(f)

# ---------------------- LOAD MOVIES DATA ----------------------
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = load_similarity()

# ---------------------- FETCH MOVIE DETAILS (OMDB API) ----------------------
def fetch_movie_data(movie_title):
    api_key = "e39708f0"   # OMDb API Key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"

    for _ in range(3):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            poster = data.get("Poster", "N/A")
            year = data.get("Year", "N/A")
            genre = data.get("Genre", "N/A")

            if poster == "N/A":
                poster = "https://via.placeholder.com/500x750?text=No+Image"

            return poster, year, genre

        except requests.exceptions.RequestException:
            time.sleep(2)

    return "https://via.placeholder.com/500x750?text=Error", "N/A", "N/A"

# ---------------------- RECOMMEND FUNCTION ----------------------
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        poster, year, genre = fetch_movie_data(title)
        recommendations.append((title, poster, year, genre))

    return recommendations

# ---------------------- STREAMLIT UI ----------------------
st.title("🎬 Movie Recommender System")
st.markdown("<h3>Find similar movies based on your favorite one!</h3>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    "Choose a movie:",
    movies["title"].values
)

if st.button("Recommend"):
    results = recommend(selected_movie_name)
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            title, poster, year, genre = results[idx]
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{poster}" width="150" style="border-radius:10px;">
                    <div class="movie-title">{title}</div>
                    <div class="movie-info">📅 {year}</div>
                    <div class="movie-info">🎭 {genre}</div>
                </div>
            """, unsafe_allow_html=True)
