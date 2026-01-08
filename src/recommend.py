import pickle
import pandas as pd


# ---------- Load Saved Data ----------

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)


# ---------- Recommendation Function ----------

def recommend(movie_name, top_n=5):
    if movie_name not in movies['title'].values:
        return []

    index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[index]

    movie_indices = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1: top_n + 1]

    return [movies.iloc[i[0]].title for i in movie_indices]


# ---------- Test ----------

if __name__ == "__main__":
    print(recommend("Batman Begins"))
