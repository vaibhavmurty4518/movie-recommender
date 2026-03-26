import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(page_title="Netflix Recommender", layout="wide")

# ---------------- UI STYLE ---------------- #
st.markdown("""
<style>

/* MAIN BACKGROUND - DARK GRADIENT */
.stApp {
    background: linear-gradient(135deg, #0f0f0f, #1a1a1a, #000000);
}

/* GLASS EFFECT CARDS */
.block-container {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border-radius: 15px;
    padding: 20px;
}

/* TITLE */
.title {
    text-align: center;
    font-size: 50px;
    color: white;
    font-weight: bold;
}

/* INPUT BOX (GLASS LOOK) */
input, .stTextInput>div>div>input {
    background: rgba(255,255,255,0.1) !important;
    color: white !important;
    border-radius: 10px !important;
}

/* SELECT BOX */
div[data-baseweb="select"] {
    background: rgba(255,255,255,0.1) !important;
    backdrop-filter: blur(10px);
    border-radius: 10px !important;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(135deg, #e50914, #b20710);
    color: white;
    border-radius: 10px;
    border: none;
}

/* HOVER EFFECT */
img {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-radius: 10px;
}
img:hover {
    transform: scale(1.08);
    box-shadow: 0px 10px 30px rgba(255,0,0,0.3);
}

/* TEXT */
.stMarkdown {
    color: white;
}

</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    movies_dict = pickle.load(open('movie_dict.pkl','rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl','rb'))
    return movies, similarity

movies, similarity = load_data()
# ---------------- SESSION STATE ---------------- #
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# ---------------- API KEY ---------------- #
API_KEY = "a9204951e9ef3720fedf404b01448c97"

# ---------------- FETCH DETAILS ---------------- #
@st.cache_data(show_spinner=False)
def fetch_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=videos,watch/providers"
        data = requests.get(url).json()

        poster_path = data.get('poster_path')
        poster = "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else None

        rating = data.get('vote_average', "N/A")

        # Trailer
        trailer = None
        if 'videos' in data:
            for v in data['videos']['results']:
                if v['type'] == 'Trailer' and v['site'] == 'YouTube':
                    trailer = f"https://www.youtube.com/watch?v={v['key']}"
                    break

        # OTT
        ott = "N/A"
        providers = data.get('watch/providers', {}).get('results', {})
        if 'IN' in providers:
            flatrate = providers['IN'].get('flatrate')
            if flatrate:
                ott = ", ".join([p['provider_name'] for p in flatrate])

        return poster, rating, trailer, ott

    except:
        return None, "N/A", None, "N/A"

# ---------------- RECOMMEND ---------------- #
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(list(enumerate(distances)),
                        reverse=True,
                        key=lambda x: x[1])[1:9]

    results = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        poster, rating, trailer, ott = fetch_details(movie_id)
        results.append((movies.iloc[i[0]].title, poster, rating, trailer, ott))

    return results

# ---------------- SEARCH ---------------- #
selected_movie = st.selectbox(
    "🎬 Choose a movie",
    movies['title'].values
)
selected_movie = selected_movie or st.selectbox("Select Movie", movies['title'].values)

# ---------------- RECOMMEND BUTTON ---------------- #
if st.button("Recommend 🎯"):
    results = recommend(selected_movie)

    cols = st.columns(5)

    for i, (title, poster, rating, trailer, ott) in enumerate(results):
        with cols[i % 5]:

            if poster:
                st.image(poster)
            else:
                st.write("No Image")

            st.markdown(f"**{title}**")
            st.markdown(f"⭐ {rating}")
            st.markdown(f"📺 {ott}")

            if trailer:
                st.markdown(f"[▶ Trailer]({trailer})")

            # ❤️ Add to favorites
            if st.button(f"❤️ Add {i}"):
                if title not in st.session_state.favorites:
                    st.session_state.favorites.append(title)

# ---------------- FAVORITES ---------------- #
st.sidebar.title("❤️ Favorites")

if st.session_state.favorites:

    for i, title in enumerate(st.session_state.favorites):

        movie_id = movies[movies['title'] == title].iloc[0].movie_id
        poster, rating, trailer, ott = fetch_details(movie_id)

        st.sidebar.markdown(f"**{title}**")
        st.sidebar.markdown(f"⭐ {rating}")

        # remove button
        if st.sidebar.button(f"❌ Remove {i}"):
            st.session_state.favorites.remove(title)
            st.rerun()

        st.sidebar.markdown("---")

else:
    st.sidebar.write("No favorites yet")
# ---------------- TRENDING ---------------- #
st.subheader("🔥 Trending Movies")
import random

def get_trending():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}"
    data = requests.get(url).json()

    movie_ids = [m['id'] for m in data['results']]

    random.shuffle(movie_ids)  # 🔥 random every time

    return movie_ids[:10]

import random

if st.button("🔄 Refresh Trending"):
    st.rerun()

trending_ids = get_trending()

cols = st.columns(5)

for i, movie_id in enumerate(trending_ids):
    poster, rating, trailer, ott = fetch_details(movie_id)

    with cols[i % 5]:
        if poster:
            st.image(poster)

        st.markdown(f"⭐ {rating}")
        st.markdown(f"📺 {ott}")

        if trailer:
            st.markdown(f"[▶ Trailer]({trailer})")