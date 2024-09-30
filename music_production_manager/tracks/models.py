from django.db import models

class Track(models.Model):
    title = models.CharField(max_length=100)
    spotify_url = models.URLField(blank=True, null=True)
    flp_file_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Project(models.Model):
    STATUS_CHOICES = [
        ('IDEA', 'アイデア段階'),
        ('PROGRESS', '進行中'),
        ('MIXING', 'ミキシング中'),
        ('MASTERING', 'マスタリング中'),
        ('COMPLETED', '完了'),
    ]
    
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.track.title} - {self.status}"