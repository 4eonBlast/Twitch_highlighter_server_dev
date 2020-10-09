import requests
import json
import re
import math
import os
import shutil
import subprocess
import ffmpeg
import time
# import ffmepg binary file in bin folder!!
client_id = "uc4dkdk0aam0pqtmmeujj6ztl5uqmp"
client_secret = "rnz2ayo0vhraicw2s1lop8nn4jg7qn"
params = {}
headers = {}
headers['Client-ID'] = client_id
headers['Authorization'] = "Bearer "

# tests
# https://www.twitch.tv/videos/746793334


def get_access_token():
    oauth_base = "https://id.twitch.tv/oauth2/token?"
    oauth_grant = "&grant_type=client_credentials"
    oauth_url = oauth_base + "client_id=" + client_id + \
        "&" + "client_secret=" + client_secret + oauth_grant

    token = requests.post(oauth_url).json()
    return token['access_token']


def get_stream_info(video_id):
    base_url = "https://api.twitch.tv/helix/videos?id="
    url = base_url+video_id
    headers['Authorization'] += get_access_token()
    req = requests.get(url, params, headers=headers)

    if 400 <= req.status_code < 500:
        return req.status_code
    req.raise_for_status()
    video_info = req.json()

    return video_info["data"][0]


def get_vid_duration(vid_info):
    duration = vid_info["duration"]

    if 'h' not in duration:
        duration = re.split('h|m|s', duration)
        duration.insert(0, "")
    elif 'h' in duration:
        duration = (re.split('h|m|s', duration))
        if len(duration) > 3:
            l = len(duration)
            l = l-3
            del duration[-l]

    elif 's' not in duration:
        duration = (re.split('h|m|s', duration))
        duration.insert(2, "")

    elif 'm' not in duration:
        duration = re.split('h|m|s', duration)
        duration.insert(1, "")

    hour = int(duration[0])
    minute = int(duration[1])
    second = int(duration[0])

    hour = hour*60
    minute = hour+minute
    second = (minute*60) + second
    total_ts_files = (second/10) + 10:
    total_ts_files = math.ceil(total_ts_files)
    return total_ts_files


def parse_thumnail_url(thumbnail):
    url = (re.split('_|/', thumbnail))
    print(url)
    # https://static-cdn.jtvnw.net/cf_vods/d2nvs31859zcd8/d78cb47810da675e8ca0_tmxk319_39714939902_1600257003//thumb/thumb0-%{width}x%{height}.jpg
    # 썸네일 주소 기준//  스트리머 아이디, 왼쪽, 오른쪽 1 , 오른쪽 2칸 데이터가 url 주소
    url1 = url[6]
    streamer_id = url[7]
    url2 = url[8]
    url3 = url[9]

    return url1, streamer_id, url2, url3


def create_req_urls(vid_info, ts_urls):
    # ts_urls 나중에 10초단위로 하이라이트 구간담은 list형식으로 전송.
    url_1, str_id, url_2, url_3 = parse_thumnail_url(vid_info["thumbnail_url"])

    ts_url_list = []
    urls_done = 0
    for _ in range(ts_urls):
        urls_done = str(urls_done)
        url = "https://d2nvs31859zcd8.cloudfront.net/" + url_1 + "_" + \
            str_id + "_" + url_2 + "_" + url_3 + "/720p60/" + urls_done + ".ts"

        ts_url_list.append(url)
        urls_done = int(urls_done)
        urls_done += 1

    return ts_url_list


def make_dir(data):
    directory = data["user_name"]
    try:
        os.mkdir("videos")
    except:
        pass

    try:
        os.mkdir("videos/" + directory)
    except:
        pass

    directory = "videos/" + directory+"/"+data["id"]
    try:
        os.mkdir(directory)
    except:
        pass

    return directory


def join_videos(test_dir, vid_num):

    vid_files = os.listdir(test_dir)
    vid_files = [s[:-3] for s in vid_files]
    vid_files.sort(key=int)
    vid_files = [s+'.ts' for s in vid_files]

    try:
        os.remove('ffmpeg.txt')
        os.remove('output.mp4')
    except:
        pass

    for item in vid_files:
        with open('ffmpeg.txt', 'a') as f:
            f.write('file '+"'"+test_dir+'/'+item+"'")
            f.write('\n')

    # join videos
    subprocess.call(
        'ffmpeg -f concat -safe 0 -i ffmpeg.txt -c copy output.mp4', shell=True)
    shutil.move('output.mp4', test_dir + '/' + vid_num + '.mp4')
    os.remove("ffmpeg.txt")
    for file in os.listdir(test_dir):
        if '.ts' in file:
            os.remove(test_dir+'/' + file)
    print("done")


def download(vid_num):
    vid_info = get_stream_info(vid_num)
    print(vid_info)
    total_ts_files = get_vid_duration(vid_info)
    print(total_ts_files)

    ts_url_list = create_req_urls(vid_info, total_ts_files)

#    for i in range(total_ts_files):
#        print(ts_url_list[i])

    test_dir = make_dir(vid_info)
    # test
    for i in range(60):
        url = requests.get(ts_url_list[i], stream=True, headers=headers)
        file_name = re.split('/', ts_url_list[i])
        file_name = file_name[5]
        if url.ok:
            with open(test_dir + '/' + file_name, 'wb') as out_file:
                shutil.copyfileobj(url.raw, out_file)

    join_videos(test_dir, vid_num)

    return
