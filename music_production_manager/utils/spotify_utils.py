# utils/spotify_utils.py
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings

def get_spotify_client():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_artist_id(track):
    return track['artists'][0]['id']

def get_related_artists(sp, artist_id):
    related_artists = sp.artist_related_artists(artist_id)
    return related_artists

def get_track_info(track_url):
    try:
        sp = get_spotify_client()
        track_result = sp.track(track_url)
        artist_name = track_result['album']['artists'][0]['name']
        track_name = track_result['name']
        artist_id = get_artist_id(track_result)
        related_artists = get_related_artists(sp, artist_id)
        related_artists_names = [artist['name'] for artist in related_artists['artists'][:5]]  # 最初の5つのみ

        track_info = sp.audio_features(track_url)
        key = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][track_info[0]['key']]
        mode = ['major', 'minor'][track_info[0]['mode']]
        bpm = round(track_info[0]['tempo'], 2)

        artist_uri = track_result['album']['artists'][0]['uri']
        artist_info = sp.artist(artist_uri)
        genres = artist_info['genres'][:5]  # 最初の5つのジャンルのみ

        data = {
            "artist_name": artist_name,
            "track_name": track_name,
            "key": key,
            "mode": mode,
            "bpm": bpm,
            "genres": genres,
            "related_artists": related_artists_names
        }
        return data

    except Exception as e:
        return f"エラーが発生しました: {e}"