from django.urls import path

from . import views

urlpatterns = [
    path('', views.track_list, name='track_list'),
    path('track/<int:pk>/', views.track_detail, name='track_detail'),
    path('track/new/', views.track_create, name='track_create'),
    path('track/<int:pk>/edit/', views.track_edit, name='track_edit'),
    path('track/<int:pk>/delete/', views.track_delete, name='track_delete'),
]