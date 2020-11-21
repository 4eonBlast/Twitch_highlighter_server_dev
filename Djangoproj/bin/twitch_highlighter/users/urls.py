from django.urls import path

from .views import home, register, search
urlpatterns = [
    path('register/', register, name='register'),
    path('', home, name='home'),
    path('search/', search, name='video_search')
]
