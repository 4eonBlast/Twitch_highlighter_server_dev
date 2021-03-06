from django.urls import path

from .import views

urlpatterns = [
    path('getvid/', views.get_vid, name='get_vid'),
    path('getchat/', views.get_vid_chat, name='get_vid_chat'),
    path('videolist/', views.video_list, name='video_list'),
    path('videolist/<int:streamer_id>',
         views.video_filt_by_streamer, name='video_list_filt'),
    path('<int:video_id>', views.video_detail, name='video_detail'),
    path('comment/write', views.comment_write, name='comment_write'),
    path('post_like/', views.post_like, name='post_like'),
]
