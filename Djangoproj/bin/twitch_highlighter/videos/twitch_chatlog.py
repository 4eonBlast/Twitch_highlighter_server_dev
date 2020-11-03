import requests
import json
import re
import csv
from os.path import dirname, join
from .models import Videos

current_dir = dirname(__file__)


def get_chatlog(video_num, test_dir):

    init_url = "https://api.twitch.tv/v5/videos/"
    url = init_url + str(video_num)+'/comments?'
    start = "content_offset_seconds=0"
    start_url = url+start

    params = {}
    params['client-id'] = "uc4dkdk0aam0pqtmmeujj6ztl5uqmp"  # 내 클라이언트 아이디
    s = requests.session()
    my_data = s.get(start_url, headers=params)
    json_data = json.loads(my_data.text)
    file_name = video_num+'.csv'
    count = 0

    while(("_next" in json_data.keys())):

        with open(test_dir+'/'+file_name, 'a') as wf:
            wc = csv.writer(wf)
            for i, commentor in enumerate(json_data["comments"], 0):
                commentor_nick = commentor['commenter']['display_name']
                comment = commentor['message']['body']
                comment_time = commentor['content_offset_seconds']
                com_list = [commentor_nick, comment, comment_time]
                if commentor_nick == "Nightbot":
                    continue
                else:
                    wc.writerow(com_list)

        next_url = url + "cursor=" + json_data['_next']
        my_data = s.get(next_url, headers=params)
        json_data = json.loads(my_data.text)
        print(count)
        count += 1

        if count == 10:
            break       # for django test

    print("complete!")

    return 1
