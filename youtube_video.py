# pytube, pytube3 순서로 pip install
# 간단하게 만들라고 opensource 사용
from pytube import YouTube
import os
import subprocess

def youtube_video_download(request_url):
    vid_data = YouTube(request_url)
    print(vid_data.length)
    # 비디오 길이가 길게 나옴
    youtuber = vid_data.author
    filename = vid_data.title
    vid_streams = vid_data.streams
    # itag에 따라서 화질, 프레임 별 영상 다운로드 가능
    # print 문 풀어서 돌려보면 선택지 여러개 나옴
    # 디폴트값은 i=3 번째 일때의 영상 선택하기로.. 보통 720p 30fps 동영상인듯
    try:
        os.mkdir("YoutubeVideo")
    except:
        pass

    directory = "YoutubeVideo/"+youtuber
    try:
        os.mkdir(directory)
    except:
        pass

    vid_streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by(
        'resolution').desc().first().download(output_path=directory, filename=filename+'video')
    vid_streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by(
        'abr').desc().first().download(output_path=directory, filename=filename+'audio')

    #workdir = os.path.dirname(os.path.realpath(__file__))+'/'+directory

    # subprocess.Popen(['ffmpeg', '-y', '-i', workdir + '/video.mp4', '-i', workdir + '/audio.mp4',
    #                   workdir + '/' + filename.replace('/', '-') + '.mp4'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #shutil.move('output.mp4', test_dir + '/' + vid_num + '.mp4')

    # os.remove(workdir+'/'+'audio.mp4')
    # os.remove(workdir+'/'+'video.mp4')

    # audio video 합치기 -- 생각보다 오래걸림

    return


request_url = "https://www.youtube.com/watch?v=X2W8jTs7mzo"  # url input
youtube_video_download(request_url)
