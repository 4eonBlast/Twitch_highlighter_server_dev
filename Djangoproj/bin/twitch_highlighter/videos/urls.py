from django.urls import path

from .import views

urlpatterns = [
    path('getvid/', views.get_vid, name='get_vid'),
    path('getchat/', views.get_vid_chat, name='get_vid_chat'),
    path('videolist/', views.video_list, name='vidio_list')
]
