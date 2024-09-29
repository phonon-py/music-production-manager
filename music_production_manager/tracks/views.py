from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Track
from .forms import TrackForm

def track_list(request):
    tracks = Track.objects.all()
    return render(request, 'tracks/track_list.html', {'tracks': tracks})

def track_detail(request, pk):
    track = get_object_or_404(Track, pk=pk)
    return render(request, 'tracks/track_detail.html', {'track': track})

def track_create(request):
    if request.method == "POST":
        form = TrackForm(request.POST)
        if form.is_valid():
            track = form.save()
            return redirect('track_detail', pk=track.pk)
    else:
        form = TrackForm()
    return render(request, 'tracks/track_form.html', {'form': form})

def track_edit(request, pk):
    track = get_object_or_404(Track, pk=pk)
    if request.method == "POST":
        form = TrackForm(request.POST, instance=track)
        if form.is_valid():
            track = form.save()
            return redirect('track_detail', pk=track.pk)
    else:
        form = TrackForm(instance=track)
    return render(request, 'tracks/track_form.html', {'form': form})

def track_delete(request, pk):
    track = get_object_or_404(Track, pk=pk)
    if request.method == "POST":
        track.delete()
        return redirect('track_list')
    return render(request, 'tracks/track_confirm_delete.html', {'track': track})