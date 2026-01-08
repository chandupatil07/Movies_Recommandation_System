import pandas as pd
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer


# ---------- Helper Functions ----------

def convert(text):
    return [i['name'] for i in ast.literal_eval(text)]


def convert_cast(text):
    return [i['name'] for i in ast.literal_eval(text)[:3]]


def fetch_director(text):
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            return [i['name']]
    return []


def stem(text):
    ps = PorterStemmer()
    return " ".join([ps.stem(word) for word in text.split()])


# ---------- Main Preprocessing ----------

def preprocess_data(movies_path, credits_path):
    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)

    credits = credits[['movie_id', 'title', 'cast', 'crew']]
    movies = movies.merge(credits, on='title')

    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    movies = movies[movies['overview'].notna()]

    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert_cast)
    movies['crew'] = movies['crew'].apply(fetch_director)

    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    for col in ['genres', 'keywords', 'cast', 'crew']:
        movies[col] = movies[col].apply(lambda x: [i.replace(" ", "") for i in x])

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast']
    new_df = movies[['movie_id', 'title', 'tags']]
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())
    new_df['tags'] = new_df['tags'].apply(stem)

    return new_df


# ---------- Vectorization & Similarity ----------

def create_similarity(new_df):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()
    similarity = cosine_similarity(vectors)
    return similarity


# ---------- Save Files ----------

def save_files(new_df, similarity):
    pickle.dump(new_df.to_dict(), open('movie_dict.pkl', 'wb'))
    pickle.dump(similarity, open('similarity.pkl', 'wb'))


# ---------- Run Pipeline ----------

if __name__ == "__main__":
    df = preprocess_data(
        'data/tmdb_5000_movies.csv',
        'data/tmdb_5000_credits.csv'
    )
    similarity = create_similarity(df)
    save_files(df, similarity)
    print("Preprocessing completed. Files saved.")
