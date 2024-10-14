from datetime import timedelta

from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import ProjectForm, TrackForm, TrackProjectForm
from .models import Platform, Project, Sale, Track, SpotifyInfo
from utils.spotify_utils import get_track_info


def track_list(request):
    tracks = Track.objects.all().order_by('-created_at')

    search_query = request.GET.get('search', '')
    if search_query:
        tracks = tracks.filter(
            Q(title__icontains=search_query) |
            Q(spotify_url__icontains=search_query)
        )

    status_filter = request.GET.get('status', '')
    if status_filter:
        tracks = tracks.filter(project__status=status_filter)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # 日付処理を行う前に、元の値を保存
    original_end_date = end_date

    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        if start_date and end_date:
            # クエリ用に終了日を翌日の0時に設定
            query_end_date = end_date + timedelta(days=1)
            tracks = tracks.filter(created_at__range=[start_date, query_end_date])

    return render(request, 'tracks/track_list.html', {
        'tracks': tracks,
        'search_query': search_query,
        'status_filter': status_filter,
        'start_date': start_date,
        'end_date': original_end_date,  # 元の終了日を使用
        'status_choices': Project.STATUS_CHOICES,
    })

def track_detail(request, pk):
    track = get_object_or_404(Track, pk=pk)
    project = track.project_set.first()
    platforms = track.platforms.all()
    spotify_info = SpotifyInfo.objects.filter(track=track).first()
    return render(request, 'tracks/track_detail.html', {
        'track': track, 
        'project': project, 
        'platforms': platforms,
        'spotify_info': spotify_info
    })

def track_create(request):
    if request.method == "POST":
        form = TrackProjectForm(request.POST)
        if form.is_valid():
            track = Track.objects.create(
                title=form.cleaned_data['title'],
                spotify_url=form.cleaned_data['spotify_url'],  # これは既に整形されています
                flp_file_path=form.cleaned_data['flp_file_path']
            )
            Project.objects.create(
                track=track,
                status=form.cleaned_data['status']
            )
            track.platforms.set(form.cleaned_data['platforms'])
            
            # Spotify情報を取得して保存
            if form.cleaned_data['spotify_url']:
                spotify_data = get_track_info(form.cleaned_data['spotify_url'])
                if isinstance(spotify_data, dict):
                    SpotifyInfo.objects.create(
                        track=track,
                        artist_name=spotify_data['artist_name'],
                        track_name=spotify_data['track_name'],
                        key=spotify_data['key'],
                        mode=spotify_data['mode'],
                        bpm=spotify_data['bpm'],
                        genres=','.join(spotify_data['genres']),
                        related_artists=','.join(spotify_data['related_artists'])
                    )
            
            return redirect('track_detail', pk=track.pk)
    else:
        form = TrackProjectForm()
    return render(request, 'tracks/track_form.html', {'form': form})

def track_edit(request, pk):
    track = get_object_or_404(Track, pk=pk)
    project = track.project_set.first()
    if request.method == "POST":
        form = TrackProjectForm(request.POST)
        if form.is_valid():
            track.title = form.cleaned_data['title']
            track.spotify_url = form.cleaned_data['spotify_url']  # これは既に整形されています
            track.flp_file_path = form.cleaned_data['flp_file_path']
            track.save()
            if project:
                project.status = form.cleaned_data['status']
                project.save()
            else:
                Project.objects.create(
                    track=track,
                    status=form.cleaned_data['status']
                )
            track.platforms.set(form.cleaned_data['platforms'])
            
            # Spotify情報を更新
            if form.cleaned_data['spotify_url']:
                spotify_data = get_track_info(form.cleaned_data['spotify_url'])
                if isinstance(spotify_data, dict):
                    SpotifyInfo.objects.update_or_create(
                        track=track,
                        defaults={
                            'artist_name': spotify_data['artist_name'],
                            'track_name': spotify_data['track_name'],
                            'key': spotify_data['key'],
                            'mode': spotify_data['mode'],
                            'bpm': spotify_data['bpm'],
                            'genres': ','.join(spotify_data['genres']),
                            'related_artists': ','.join(spotify_data['related_artists'])
                        }
                    )
            
            return redirect('track_detail', pk=track.pk)
    else:
        initial_data = {
            'title': track.title,
            'spotify_url': track.spotify_url,
            'flp_file_path': track.flp_file_path,
            'status': project.status if project else '',
            'platforms': track.platforms.all()
        }
        form = TrackProjectForm(initial=initial_data)
    return render(request, 'tracks/track_form.html', {'form': form, 'track': track})

def track_delete(request, pk):
    track = get_object_or_404(Track, pk=pk)
    if request.method == "POST":
        track.delete()
        return redirect('track_list')
    return render(request, 'tracks/track_confirm_delete.html', {'track': track})

@require_POST
@csrf_exempt
def get_spotify_info(request):
    data = json.loads(request.body)
    spotify_url = data.get('spotify_url')
    if spotify_url:
        spotify_data = get_track_info(spotify_url)  # この行を確認してください
        if isinstance(spotify_data, dict):
            return JsonResponse(spotify_data)
        else:
            return JsonResponse({'error': str(spotify_data)})
    return JsonResponse({'error': 'No Spotify URL provided'})