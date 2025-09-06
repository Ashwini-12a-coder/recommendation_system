import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "79f6f5c07f9e48aa9f18aa64159c1848"
CLIENT_SECRET = "4cab7aa8dd5c4b35a63702b2a73e04fb"

# Initialize Spotify client with timeout and retries
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)
sp = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager,
    requests_timeout=30,  # wait longer before timeout
    retries=5             # retry if request fails
)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    try:
        results = sp.search(q=search_query, type="track", limit=1)
        if results and results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            return track["album"]["images"][0]["url"]
        else:
            return "https://i.postimg.cc/00NxYz4V/social.png"  # default image
    except Exception as e:
        print("Spotify API error:", e)
        return "https://i.postimg.cc/00NxYz4V/social.png"  # fallback image

def recommend(song):
    # Find the index of the song
    index = music[music['song'] == song].index[0]

    # Get similarity scores and sort descending
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_music_names = []
    recommended_music_posters = []

    for i in distances[1:6]:  # top 5 recommendations excluding the song itself
        idx = i[0]
        artist = music.iloc[idx].artist
        song_name = music.iloc[idx].song

        recommended_music_posters.append(get_song_album_cover_url(song_name, artist))
        recommended_music_names.append(song_name)

    return recommended_music_names, recommended_music_posters

# Load data once
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.header('🎵 MUSIC RECOMMENDER SYSTEM 🎶')

music_list = music['song'].values
selected_song = st.selectbox("Type or select a song from the dropdown", music_list)

if st.button("Show Recommendation"):
    recommended_music_names, recommended_music_posters = recommend(selected_song)

    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(recommended_music_names[i])
            st.image(recommended_music_posters[i])
