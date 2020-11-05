from __future__ import absolute_import, unicode_literals
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import Streamer, Videos
from .forms import VidInputForm
from django.views.decorators.csrf import csrf_exempt
import re
import os
from .twitch_chatlog import get_chatlog
from .twitch_video import download_vid, get_stream_info
from celery import shared_task
# from .tasks import get_chatlog
# videos model에 저장해야됨
# download video 기능에서 더 추가 필요//
# https://www.twitch.tv/videos/781069869
# https://www.twitch.tv/videos/781288596


def make_dir(data):
    directory = data["user_name"]
    try:
        os.mkdir("media/video")
    except:
        pass

    try:
        os.mkdir("media/video/" + directory)
    except:
        pass

    directory = "media/video/" + directory+"/"+data["id"]
    try:
        os.mkdir(directory)
    except:
        pass

    return directory


@shared_task
def create_video(video_num, dir_name, video_id):

    get_chatlog(video_num, dir_name)
    download_vid(video_num, dir_name)
    video = Videos.objects.get(pk=video_id)
    video.vid_file = dir_name[6:]+"/"+video_num+".mp4"
    video.save()


def get_vid(request):

    if request.method == 'GET':
        vidurl_form = VidInputForm()
        return render(request, 'registration/getvidurl.html', {'vidurl_form': vidurl_form})

    if request. method == 'POST':

        return HttpResponse("<div>Hello!</div>")


@csrf_exempt
def get_vid_chat(request):

    if request.method == 'POST':
        req_url = request.POST.get('vid_url')
        print(req_url)
        # 여기서 req_url 확인 후, twitch replay url이 아니라면 error를 보내는// (redirect에)

        inputurl_num = re.findall("\\d+", req_url)
        video_num = "".join(inputurl_num)
        vid_info = get_stream_info(video_num)
        print(vid_info)
        if str(type(vid_info)) != "<class 'dict'>":
            error = "Invalid Replay URL!"
            return render(request, 'registration/getvidurl.html', {'error': error})

        if Streamer.objects.filter(streamer_name=vid_info["user_name"]):
            streamer = Streamer.objects.get(
                streamer_name=vid_info["user_name"])
        else:
            streamer = Streamer.objects.create(
                streamer_name=vid_info["user_name"])
            streamer.save()

        if Videos.objects.filter(vid_num=vid_info["id"]):
            return render(request, 'registration/getvidurl.html')
        else:
            video = Videos.objects.create(
                streamer_name=streamer, vid_url=req_url, vid_path='/', vid_title=vid_info["title"])
            video.save()

        dir_name = make_dir(vid_info)
        # video_save 여기서
        # 여기서 모델 생성, 채팅로그, 비디오 제작 등 작업진행
        # 비디오 서버 안에 저장?

        create_video.delay(video_num, dir_name, video.id)
        return redirect(get_vid)
    else:
        print("hello")
        return redirect(get_vid)


def video_list(request):
    videos = Videos.objects.order_by('-registered_dttm')
    streamer = Streamer.objects.order_by('streamer_name')

    return render(request, 'videopost/video_list.html', context={'videos': videos, 'streamer': streamer})


def video_filt_by_streamer(request, streamer_id):

    streamer = get_object_or_404(Streamer, pk=streamer_id)
    view_streamer = Streamer.objects.order_by('streamer_name')
    videos = Videos.objects.filter(
        streamer_name=streamer.id)
    filter_msg = streamer.streamer_name

    return render(request, 'videopost/video_list.html', context={'videos': videos, 'streamer': view_streamer, 'filter_msg': filter_msg})


def video_detail(request, video_id):
    video = get_object_or_404(Videos, pk=video_id)

    return render(request, 'videopost/video_detail.html', context={'video': video})

# https://www.twitch.tv/videos/789379470
# https://www.twitch.tv/videos/786290534
