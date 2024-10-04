from django import forms
from .models import Track, Project

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'spotify_url', 'flp_file_path']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['status']

class TrackProjectForm(forms.Form):
    title = forms.CharField(max_length=100)
    spotify_url = forms.URLField(required=False)
    flp_file_path = forms.CharField(max_length=255, required=False)
    status = forms.ChoiceField(choices=Project.STATUS_CHOICES)