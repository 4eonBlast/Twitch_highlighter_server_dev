from django.urls import path

from .views import home, register
urlpatterns = [
    path('register/', register, name='register'),
    path('', home, name='home')
]
