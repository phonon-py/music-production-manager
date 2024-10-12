from datetime import timedelta

from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date

from .forms import ProjectForm, TrackForm, TrackProjectForm
from .models import Platform, Project, Sale, Track


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
    return render(request, 'tracks/track_detail.html', {'track': track, 'project': project, 'platforms': platforms})

def track_create(request):
    if request.method == "POST":
        form = TrackProjectForm(request.POST)
        if form.is_valid():
            track = Track.objects.create(
                title=form.cleaned_data['title'],
                spotify_url=form.cleaned_data['spotify_url'],
                flp_file_path=form.cleaned_data['flp_file_path']
            )
            Project.objects.create(
                track=track,
                status=form.cleaned_data['status']
            )
            track.platforms.set(form.cleaned_data['platforms'])
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
            track.spotify_url = form.cleaned_data['spotify_url']
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
    return render(request, 'tracks/track_form.html', {'form': form})

def track_delete(request, pk):
    track = get_object_or_404(Track, pk=pk)
    if request.method == "POST":
        track.delete()
        return redirect('track_list')
    return render(request, 'tracks/track_confirm_delete.html', {'track': track})