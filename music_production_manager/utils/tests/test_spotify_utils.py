from django.test import TestCase
from django.conf import settings
from unittest.mock import patch, MagicMock
from utils.spotify_utils import get_spotify_client, get_artist_id, get_related_artists, get_track_info

class SpotifyUtilsTestCase(TestCase):

    @patch('utils.spotify_utils.SpotifyClientCredentials')
    @patch('utils.spotify_utils.spotipy.Spotify')
    def test_get_spotify_client(self, mock_spotify, mock_credentials):
        client = get_spotify_client()
        mock_credentials.assert_called_once_with(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET
        )
        mock_spotify.assert_called_once()

    def test_get_artist_id(self):
        mock_track = {'artists': [{'id': '123'}]}
        self.assertEqual(get_artist_id(mock_track), '123')

    @patch('utils.spotify_utils.get_spotify_client')
    def test_get_related_artists(self, mock_get_client):
        mock_sp = MagicMock()
        mock_sp.artist_related_artists.return_value = {'artists': [{'name': 'Artist1'}, {'name': 'Artist2'}]}
        mock_get_client.return_value = mock_sp

        result = get_related_artists(mock_sp, '123')
        self.assertEqual(result, {'artists': [{'name': 'Artist1'}, {'name': 'Artist2'}]})
        mock_sp.artist_related_artists.assert_called_once_with('123')

    @patch('utils.spotify_utils.get_spotify_client')
    def test_get_track_info(self, mock_get_client):
        mock_sp = MagicMock()
        mock_sp.track.return_value = {
            'album': {'artists': [{'name': 'Test Artist', 'uri': 'spotify:artist:123'}]},
            'name': 'Test Track',
            'artists': [{'id': '123'}]
        }
        mock_sp.audio_features.return_value = [{'key': 0, 'mode': 1, 'tempo': 120.5}]
        mock_sp.artist_related_artists.return_value = {'artists': [{'name': 'Related1'}, {'name': 'Related2'}]}
        mock_sp.artist.return_value = {'genres': ['Genre1', 'Genre2']}
        mock_get_client.return_value = mock_sp

        result = get_track_info('spotify:track:123')
        expected = {
            'artist_name': 'Test Artist',
            'track_name': 'Test Track',
            'key': 'C',
            'mode': 'minor',
            'bpm': 120.5,
            'genres': ['Genre1', 'Genre2'],
            'related_artists': ['Related1', 'Related2']
        }
        self.assertEqual(result, expected)

    @patch('utils.spotify_utils.get_spotify_client')
    def test_get_track_info_error(self, mock_get_client):
        mock_get_client.side_effect = Exception('Test error')
        result = get_track_info('spotify:track:123')
        self.assertEqual(result, "エラーが発生しました: Test error")