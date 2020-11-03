from django.urls import path

from .import views

urlpatterns = [
    path('getvid/', views.get_vid, name='get_vid'),
    path('getchat/', views.get_vid_chat, name='get_vid_chat'),
    path('videolist/', views.video_list, name='video_list'),
    path('<int:video_id>', views.video_detail, name='video_detail'),
]
