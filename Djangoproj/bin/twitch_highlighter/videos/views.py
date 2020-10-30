from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import Streamer, Videos
from .forms import VidInputForm
from django.views.decorators.csrf import csrf_exempt
import re
from .twitch_chatlog import get_chatlog
from .twitch_video import download_vid, get_stream_info
#from .tasks import get_chatlog
# videos model에 저장해야됨
# download video 기능에서 더 추가 필요//


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

        if 400 <= vid_info < 500:
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
            pass
        else:
            video = Videos.objects.create(
                streamer_name=streamer, vid_url=req_url, vid_path='/')
            video.save()

        # get_chatlog.delay(req_url)
        download_vid.delay("764048201")
        # video_save 여기서
        # 여기서 모델 생성, 채팅로그, 비디오 제작 등 작업진행
        # 비디오 서버 안에 저장?

        return redirect(get_vid)
    else:
        print("hello")
        return redirect(get_vid)


def video_list(request):
    videos = Videos.objects.order_by('-registered_dttm')

    return render(request, 'videopost/video_list.html', context={'videos': videos})


# def video_detail(request):
