import pickle
import streamlit as st
import requests


# -------------------------------
# TMDB API
# -------------------------------
TMDB_API_KEY = "ca115159d2852bfb15dc15b88e78ec16",


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": "ca115159d2852bfb15dc15b88e78ec16",
        "language": "en-US"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

        return None

    except requests.exceptions.RequestException as e:
        print(f"TMDB request failed for movie {movie_id}: {e}")
        return None


# -------------------------------
# Recommendation function
# -------------------------------
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:

        movie_id = movies.iloc[i[0]].movie_id

        poster = fetch_poster(movie_id)

        recommended_movie_names.append(
            movies.iloc[i[0]].title
        )

        recommended_movie_posters.append(poster)

    return recommended_movie_names, recommended_movie_posters


# -------------------------------
# Streamlit app
# -------------------------------
st.header("Movie Recommender System")

movies = pickle.load(
    open("movie_list.pkl", "rb")
)

similarity = pickle.load(
    open("similarity.pkl", "rb")
)


movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)


if st.button("Show Recommendation"):

    recommended_movie_names, recommended_movie_posters = recommend(
        selected_movie
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    columns = [col1, col2, col3, col4, col5]

    for i, col in enumerate(columns):

        with col:

            st.text(recommended_movie_names[i])

            if recommended_movie_posters[i]:
                st.image(
                    recommended_movie_posters[i]
                )
            else:
                st.write("Poster unavailable")