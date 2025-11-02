import streamlit as st
import pickle

# Load data
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

st.set_page_config(page_title="Movie Recommender", layout="centered")
st.title("🎬 Movie Recommendation System")

movie_list = movies['title'].values
selected_movie = st.selectbox("Search or choose a movie to get recommendations:", movie_list)

def recommend(movie):
    movie = movie.lower()
    index = movies[movies['title'].str.lower() == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movie_list]

if st.button("Recommend"):
    st.subheader("Recommended Movies 🎥")
    
    recommendations = recommend(selected_movie)
    for movie in recommendations:
        st.write(f"✅ {movie}")
    st.success("Enjoy your movies!")    