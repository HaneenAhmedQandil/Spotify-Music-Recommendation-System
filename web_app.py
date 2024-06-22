import pandas as pd
import streamlit as st
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify client setup
CLIENT_ID = "dcd335aa517241c693b4b20026187fb0"
CLIENT_SECRET = "e487e8331acc4b2295fe4980e13cb7de"
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
spotify = Spotify(auth_manager=auth_manager)
def fetch_spotify_url(song_name, artist_name):
    query = f"track:{song_name} artist:{artist_name}"
    search_result = spotify.search(q=query, type='track', limit=1)
    tracks = search_result.get('tracks', {}).get('items', [])
    if tracks:
        spotify_url = tracks[0]['external_urls']['spotify']
        return spotify_url
    return None
def fetch_album_cover(song_name, artist_name):
    query = f"track:{song_name} artist:{artist_name}"
    search_result = spotify.search(q=query, type='track', limit=1)
    tracks = search_result.get('tracks', {}).get('items', [])
    if tracks:
        album_cover_url = tracks[0]['album']['images'][0]['url']
        return album_cover_url
    return "https://i.postimg.cc/0QNxYz4V/social.png"

def generate_recommendations(selected_song, music_df, similarity_matrix):
    song_index = music_df[music_df['song'] == selected_song].index[0]
    similar_songs = sorted(list(enumerate(similarity_matrix[song_index])), key=lambda x: x[1], reverse=True)[1:6]
    
    recommendations = []
    for i, _ in similar_songs:
        song_info = music_df.iloc[i]
        album_cover = fetch_album_cover(song_info['song'], song_info['artist'])
        spotify_url = fetch_spotify_url(song_info['song'], song_info['artist'])  # Fetch the Spotify URL
        recommendations.append((song_info['song'], album_cover, spotify_url))
    return recommendations
# Load data
music_df = pd.read_pickle('df.pkl')
similarity_matrix = pd.read_pickle('similarity.pkl')

# Streamlit UI
st.header('Spotify Music Recommendation System')
song_list = music_df['song'].unique()
selected_song = st.selectbox("Choose a song to get recommendations:", song_list)

if st.button('Get Recommendations'):
    recommendations = generate_recommendations(selected_song, music_df, similarity_matrix)
    cols = st.columns(len(recommendations))  # Create columns for each recommendation
    for col, (song_name, album_cover, spotify_url) in zip(cols, recommendations):
        with col:  # Use the column context
            if spotify_url:  # Ensure there is a Spotify URL
                # Use Markdown to create clickable images within each column
                st.markdown(f"[![{song_name}]({album_cover})]({spotify_url})", unsafe_allow_html=True)
            else:
                st.image(album_cover, width=150, caption=song_name, use_column_width=True)