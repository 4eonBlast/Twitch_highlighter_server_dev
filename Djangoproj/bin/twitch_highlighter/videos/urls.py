from django.urls import path

from .import views

urlpatterns = [
    path('getvid/', views.get_vid, name='getvid'),
    path('getchat/', views.get_vid_chat, name='get_vid_chat'),
]
