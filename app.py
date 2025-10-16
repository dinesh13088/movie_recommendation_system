import streamlit as st
import pickle
import requests

movies=pickle.load(open('movies.pkl','rb'))
movies_list=movies['title'].values
similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response =requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=cf2d5a06bcf31cb72ec6c589490341cc&language=en-US")
    data=response.json()
    poster_path=data['poster_path']
    return "https://image.tmdb.org/t/p/w500/"+poster_path


def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distance=similarity[movie_index]

    recommend_movies=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[-1])[1:6]
    recommended_movies_poster=[]

    movies_titles=[]
    for i in recommend_movies:
        movie_id=movies.iloc[i[0]].id
        movies_titles.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id=movie_id))

    return movies_titles,recommended_movies_poster

st.title("Movie Recommendation System ")
selected = st.selectbox(
    "Select Movie?",
    movies_list,
)

if st.button("Recommend"):
    recommended_movies_title,movie_poster=recommend(selected)
    cols= st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movies_title[i])
            st.image(movie_poster[i])






