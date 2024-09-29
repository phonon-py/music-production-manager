from django.db import models

class Track(models.Model):
    title = models.CharField(max_length=100)
    spotify_url = models.URLField(blank=True, null=True)
    flp_file_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title