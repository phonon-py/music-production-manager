from django.test import TestCase
from django.urls import reverse

from .models import Track


class TrackModelTests(TestCase):
    def test_track_creation(self):
        track = Track.objects.create(title="Test Track", spotify_url="https://spotify.com/test", flp_file_path="/path/to/test.flp")
        self.assertTrue(isinstance(track, Track))
        self.assertEqual(track.__str__(), track.title)

class TrackViewTests(TestCase):
    def setUp(self):
        self.track = Track.objects.create(title="Test Track", spotify_url="https://spotify.com/test", flp_file_path="/path/to/test.flp")

    def test_track_list_view(self):
        response = self.client.get(reverse('track_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Track")

    def test_track_detail_view(self):
        response = self.client.get(reverse('track_detail', args=[self.track.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.track.title)

    def test_track_create_view(self):
        response = self.client.post(reverse('track_create'), {
            'title': 'New Track',
            'spotify_url': 'https://spotify.com/new',
            'flp_file_path': '/path/to/new.flp'
        })
        self.assertEqual(response.status_code, 302)  # リダイレクトを期待
        self.assertTrue(Track.objects.filter(title='New Track').exists())

    def test_track_update_view(self):
        response = self.client.post(reverse('track_edit', args=[self.track.id]), {
            'title': 'Updated Track',
            'spotify_url': self.track.spotify_url,
            'flp_file_path': self.track.flp_file_path
        })
        self.assertEqual(response.status_code, 302)  # リダイレクトを期待
        self.track.refresh_from_db()
        self.assertEqual(self.track.title, 'Updated Track')

    def test_track_delete_view(self):
        response = self.client.post(reverse('track_delete', args=[self.track.id]))
        self.assertEqual(response.status_code, 302)  # リダイレクトを期待
        self.assertFalse(Track.objects.filter(id=self.track.id).exists())