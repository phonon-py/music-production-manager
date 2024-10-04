from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Track, Project, Sale
from .forms import TrackForm, ProjectForm, TrackProjectForm


def track_list(request):
    # 全ての曲を取得
    tracks = Track.objects.all()

    # 検索機能
    search_query = request.GET.get('search', '')
    if search_query:
        tracks = tracks.filter(
            Q(title__icontains=search_query) |
            Q(spotify_url__icontains=search_query)
        )

    # フィルタリング機能
    status_filter = request.GET.get('status', '')
    if status_filter:
        tracks = tracks.filter(project__status=status_filter)

    # 日付範囲フィルタリング
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        tracks = tracks.filter(sale__sale_date__range=[start_date, end_date])

    # テンプレートにデータを渡す
    return render(request, 'tracks/track_list.html', {
        'tracks': tracks,
        'search_query': search_query,
        'status_filter': status_filter,
        'start_date': start_date,
        'end_date': end_date,
    })

def track_detail(request, pk):
    track = get_object_or_404(Track, pk=pk)
    return render(request, 'tracks/track_detail.html', {'track': track})

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
            return redirect('track_detail', pk=track.pk)
    else:
        form = TrackProjectForm()
    return render(request, 'tracks/track_form.html', {'form': form})

def track_edit(request, pk):
    track = get_object_or_404(Track, pk=pk)
    project = track.project_set.first()  # トラックに関連するプロジェクトを取得
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
            return redirect('track_detail', pk=track.pk)
    else:
        initial_data = {
            'title': track.title,
            'spotify_url': track.spotify_url,
            'flp_file_path': track.flp_file_path,
            'status': project.status if project else ''
        }
        form = TrackProjectForm(initial=initial_data)
    return render(request, 'tracks/track_form.html', {'form': form})

def track_delete(request, pk):
    track = get_object_or_404(Track, pk=pk)
    if request.method == "POST":
        track.delete()
        return redirect('track_list')
    return render(request, 'tracks/track_confirm_delete.html', {'track': track})