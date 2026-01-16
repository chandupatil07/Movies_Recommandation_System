# ---------------------- Fetch Poster Function ----------------------
def fetch_movie_data(movie_title):
    api_key = "e39708f0"  # your OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            poster_url = data.get("Poster")
            year = data.get("Year", "N/A")
            genre = data.get("Genre", "N/A")
            plot = data.get("Plot", "N/A")

            if not poster_url or poster_url == "N/A":
                poster_url = "https://via.placeholder.com/500x750?text=No+Image"

            return poster_url, year, genre, plot

        except requests.exceptions.RequestException:
            if attempt < 2:
                time.sleep(2)
                continue
            return "https://via.placeholder.com/500x750?text=Error", "N/A", "N/A", "N/A"


# ---------------------- Recommender Function ----------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])[1:6]

    recommended_data = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        poster, year, genre, plot = fetch_movie_data(title)
        recommended_data.append((title, poster, year, genre, plot))

    return recommended_data


# ---------------------- Load Data ----------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------------- Streamlit UI ----------------------
st.title('🎬 Movie Recommender System')
st.markdown("<h3>Find similar movies based on your favorite one!</h3>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    "Choose a movie to get similar recommendations:",
    movies['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            title, poster, year, genre, plot = recommendations[idx]
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{poster}" width="150" style="border-radius:10px;">
                    <div class="movie-title">{title}</div>
                    <div class="movie-info"> {year}</div>
                    <div class="movie-info"> {genre}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
