from django.shortcuts import render, redirect
from django.urls import reverse
from videos.models import Videos, Streamer
from django.db.models import Count
from django.core.paginator import Paginator
from videos.views import video_filt_by_streamer
# Create your views here.

from .forms import RegisterForm


def search(request):

    v = request.GET.get('v', '')
    if v:
        search = Streamer.objects.filter(streamer_name=v)
        if search.exists():
            search = Streamer.objects.get(streamer_name=v)
            return video_filt_by_streamer(request, search.id)

    sort_by_like = Videos.objects.annotate(
        like_count=Count('likes')).order_by('-like_count')

    page = int(request.GET.get('p', 1))
    paginator = Paginator(sort_by_like, 10)
    like_videos = paginator.get_page(page)

    latest = Videos.objects.all().order_by('-registered_dttm')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(latest, 10)
    latest_vid = paginator.get_page(page)
    error = "no such streamer"
    return render(request, 'registration/home.html', context={'like_videos': like_videos, 'latest_videos': latest_vid, 'error': error})


def home(request):

    sort_by_like = Videos.objects.annotate(
        like_count=Count('likes')).order_by('-like_count')

    page = int(request.GET.get('p', 1))
    paginator = Paginator(sort_by_like, 10)
    like_videos = paginator.get_page(page)

    latest = Videos.objects.all().order_by('-registered_dttm')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(latest, 10)
    latest_vid = paginator.get_page(page)

    return render(request, 'registration/home.html', context={'like_videos': like_videos, 'latest_videos': latest_vid})


def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/login.html', {'user': user})

    else:
        user_form = RegisterForm()

    return render(request, 'registration/register.html', {'user_form': user_form})
