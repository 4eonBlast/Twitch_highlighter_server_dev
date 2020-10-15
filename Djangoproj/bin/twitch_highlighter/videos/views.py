from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import Videos
from .forms import VidInputForm
from django.views.decorators.csrf import csrf_exempt

#from .tasks import get_chatlog
# videos model에 저장해야됨
# download video 기능에서 더 추가 필요//


def get_vid(request):

    if request.method == 'GET':
        vidurl_form = VidInputForm()
        return render(request, 'registration/vidurl.html', {'vidurl_form': vidurl_form})

    if request. method == 'POST':

        return HttpResponse("<div>Hello World!</div>")


@csrf_exempt
def get_vid_chat(request):

    if request.method == 'POST':
        print("hello")
        HttpResponse("hello")
        req_url = request.POST.get('vid_url')
        print(req_url)
        # 여기서 req_url 확인 후, twitch replay url이 아니라면 error를 보내는// (redirect에)

        # get_chatlog.delay(req_url)
        # 여기서 모델 생성, 채팅로그, 비디오 제작 등 작업진행
        # 비디오 서버 안에 저장?

        return redirect(get_vid)
    else:
        print("hello")
        return redirect(get_vid)

# https://www.twitch.tv/videos/761217067
# https://www.twitch.tv/videos/750800224
# https://www.twitch.tv/videos/764048201
