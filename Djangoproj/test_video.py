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

# 내일 할거
# oath_url parsing
# function 구조로 나누기
# 다운로드 속도 좀더 빠르게?

oauth_url = "https://id.twitch.tv/oauth2/token?client_id=uc4dkdk0aam0pqtmmeujj6ztl5uqmp&client_secret=rnz2ayo0vhraicw2s1lop8nn4jg7qn&grant_type=client_credentials"
# client id uc4dkdk0aam0pqtmmeujj6ztl5uqmp
# client secret "rnz2ayo0vhraicw2s1lop8nn4jg7qn"

# https://www.twitch.tv/videos/746793334


def main():
    my_token = requests.post(oauth_url).json()
    url = "https://api.twitch.tv/helix/videos?id=746793334"

    params = {}
    headers = {}
    headers['Client-ID'] = "uc4dkdk0aam0pqtmmeujj6ztl5uqmp"
    headers["Authorization"] = "Bearer " + my_token['access_token']
    response = requests.get(url, params, headers=headers)
    # print(response.text)
    if 400 <= response.status_code < 500:
        print(response.status_code)
        quit()
    response.raise_for_status()
    video_temp = response.json()
    video_info = video_temp["data"][0]
    print(video_temp)
    # print(video["data"][0]["id"])
    dur_data = get_duration(video_info)

    hour = int(dur_data[0])
    minute = int(dur_data[1])
    second = int(dur_data[0])

    hour = hour*60
    minute = hour+minute
    second = (minute*60) + second
    total_ts_files = (second/10) + 10

    total_ts_files = math.ceil(total_ts_files)
    url_1, str_id, url_2, url_3 = parse_thumnail_url(video_info)

    ts_url_list = []
    urls_done = 0

    for _ in range(total_ts_files):
        urls_done = str(urls_done)
        url = "https://d2nvs31859zcd8.cloudfront.net/" + url_1 + "_" + \
            str_id + "_" + url_2 + "_" + url_3 + "/720p60/" + urls_done + ".ts"

        ts_url_list.append(url)
        urls_done = int(urls_done)
        urls_done += 1

    # for url in ts_url_list:
    #     file_name = re.split('/', url)
    #     file_name = file_name[5]
    #     print(file_name)

    test_dir = make_dir(video_info)
    for i in range(60):
        url = requests.get(ts_url_list[i], stream=True, headers=headers)
        file_name = re.split('/', ts_url_list[i])
        file_name = file_name[5]
        if url.ok:
            with open(test_dir + '/' + file_name, 'wb') as out_file:
                shutil.copyfileobj(url.raw, out_file)

    vid_files = os.listdir(test_dir)
    print(vid_files)
    print(test_dir)

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

    print('ok5')
    time.sleep(20)
    shutil.move('output.mp4', test_dir + '/' + video_info["id"] + '.mp4')
    os.remove("ffmpeg.txt")
    for file in os.listdir(test_dir):
        if '.ts' in file:
            os.remove(test_dir+'/' + file)
    print("done")


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


def get_duration(data):
    duration = data["duration"]

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

    return duration


def parse_thumnail_url(data):
    thumbnail = data["thumbnail_url"]
    url = (re.split('_|/', thumbnail))
    print(url)
    # print(thumbnail)
    # print(username.lower())
    # username_pos = url.index("tmxk319")
    # https://static-cdn.jtvnw.net/cf_vods/d2nvs31859zcd8/d78cb47810da675e8ca0_tmxk319_39714939902_1600257003//thumb/thumb0-%{width}x%{height}.jpg
    # 썸네일 주소 기준 스트리머 아이디 왼쪽, 오른쪽 1 , 오른쪽 2칸 데이터가 url 주소
    url1 = url[6]
    streamer_id = url[7]
    url2 = url[8]
    url3 = url[9]

    return url1, streamer_id, url2, url3


if __name__ == "__main__":
    main()
