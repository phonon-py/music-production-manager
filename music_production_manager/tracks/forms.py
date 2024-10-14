from django import forms
from django.core.exceptions import ValidationError
from .models import Platform, Project, Track


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
    platforms = forms.ModelMultipleChoiceField(
        queryset=Platform.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='プラットフォーム'
    )

    def clean_spotify_url(self):
        url = self.cleaned_data.get('spotify_url')
        if url:
            # 'intl-ja' を削除
            url = url.replace('intl-ja', '')

            # URL内の '//' を '/' に置き換え
            url = url.replace('//', '/')

            # 'https:/' を 'https://' に戻す
            url = url.replace('https:/', 'https://')

            # Spotifyのトラックページのみを許可
            if not url.startswith('https://open.spotify.com/track/'):
                raise ValidationError('有効なSpotify トラックURLを入力してください。')

        return url