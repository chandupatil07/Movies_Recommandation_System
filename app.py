# I added the comments on this file so everyone can understand
import streamlit as st
import pickle
import requests
import io

# ===============================
# OMDb API Key
# ===============================
OMDB_API_KEY = "e39708f0"

# ===============================
Load Pickle from Google Drive
# ===============================
def load_pickle_from_drive(file_id):
    url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(url)
    response.raise_for_status()
    return pickle.load(io.BytesIO(response.content))

# Replace with your actual Google Drive IDs
MOVIES_FILE_ID = "YOUR_MOVIES_PKL_FILE_ID"
SIMILARITY_FILE_ID = "1IOmttRuwby4Awf4X1yLxZBzMvZd5tV51"

movies = load_pickle_from_drive(MOVIES_FILE_ID)
similarity = load_pickle_from_drive(SIMILARITY_FILE_ID)

movie_list = movies['title'].values

# ===============================
#Fetch Poster from OMDb
# ===============================
def fetch_poster(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    data = requests.get(url).json()
    poster_url = data.get("Poster")
    if poster_url and poster_url != "N/A":
        return poster_url
    return "https://via.placeholder.com/300x450?text=No+Image"

# ===============================
# Recommendation Function
# ===============================
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list_idx = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list_idx:
        movie_name = movies.iloc[i[0]].title
        recommended_movies.append(movie_name)
        recommended_posters.append(fetch_poster(movie_name))
    return recommended_movies, recommended_posters

# ===============================
# Streamlit Page Config
# ===============================
st.set_page_config(page_title=" Movie Recommendation System", layout="wide")

# ===============================
#Custom CSS
# ===============================
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1e1e2f, #252542);
        color: white;
    }
    .movie-card {
        transition: transform 0.3s, box-shadow 0.3s;
        border-radius: 15px;
        overflow: hidden;
        background: #2b2b40;
        padding: 10px;
        text-align: center;
    }
    .movie-card:hover {
        transform: scale(1.07);
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
    }
    .movie-title {
        margin-top: 10px;
        font-size: 18px;
        font-weight: bold;
        color: #f8f8f8;
    }
    img {
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# ===============================
# App Layout
# ===============================
st.title(" Movie Recommendation System")
st.write("Discover movies you’ll love. Select a movie to get recommendations!")

selected_movie = st.selectbox("Choose a movie:", movie_list)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{posters[idx]}" width="150">
                    <div class="movie-title">{names[idx]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

