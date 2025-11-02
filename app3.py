import streamlit as st
import pickle, requests, os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# Load model data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.set_page_config(page_title="Movie Recommender 🎬", layout="wide")

# Custom CSS
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f0f0f, #1c1c1c);
}

.stApp {
    background: linear-gradient(135deg, #111, #1a1a1a);
}

.movie-card {
    display: flex;
    gap: 12px;
    padding: 14px;
    border-radius: 12px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(8px);
    transition: 0.3s;
}

.movie-card:hover {
    transform: scale(1.03);
    background: rgba(255,255,255,0.12);
}

.movie-title {
    font-size: 20px;
    font-weight: 600;
    color: #fff;
}
.movie-meta {
    font-size: 14px;
    color: #ddd;
}
</style>
""", unsafe_allow_html=True)

def fetch_movie_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
    except:
      return "", "N/A", "No Data Available", []
    poster_path = data.get("poster_path", "")
    rating = data.get("vote_average", "N/A")
    overview = data.get("overview", "No description")
    watch = data.get("homepage", "")

    watch_links = []
    if "netflix" in overview.lower(): watch_links.append("✅ Netflix")
    if "amazon" in overview.lower(): watch_links.append("✅ Amazon Prime Video")
    if "hotstar" in overview.lower(): watch_links.append("✅ Hotstar")
    if "hulu" in overview.lower(): watch_links.append("✅ Hulu")

    return (
        f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
        rating,
        overview[:200] + "...",
        watch_links[:3]
    )

def recommend(movie):
    movie = movie.lower()
    index = movies[movies['title'].str.lower() == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    result = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster, rating, overview, platforms = fetch_movie_poster(movie_id)
        result.append((title, poster, rating, overview, platforms))
    return result

st.title("🍿 Movie Recommendation System")
st.write("Discover similar movies based on your choice 🎥🔥")

movie_list = movies['title'].values
selected = st.selectbox("🔎 Search a Movie", movie_list)

if st.button("Get Recommendations 🚀"):
    with st.spinner("Fetching Recommendations..."):
        recs = recommend(selected)

    st.write("### 🎬 Recommended Movies:")

    for title, poster, rating, overview, platforms in recs:
        col1, col2 = st.columns([1,3])
        with col1: 
             if poster and poster != "":
                 st.image(poster, use_container_width=True)
             else:
                 st.image("https://via.placeholder.com/300x450?text=No+Image", use_container_width=True)
        with col2:
            st.markdown(f"<div class='movie-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='movie-meta'>⭐ Rating: {rating}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='movie-meta'>{overview}</div>", unsafe_allow_html=True)

            if len(platforms) > 0:
                st.write("🎟️ Available on:")
                for p in platforms:
                    st.write(p)
            else:
                st.write("⛔ Platform info unavailable")

            st.markdown("</div>", unsafe_allow_html=True)
    st.success("Enjoy your movies! 🍿")