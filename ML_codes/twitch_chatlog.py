import requests
import json
import re
import csv
from fake_useragent import UserAgent as ua
from os.path import dirname, join
current_dir = dirname(__file__)

inputurl = input("입력 :")
print(inputurl)
inputurl_num = re.findall("\\d+", inputurl)
video_num = "".join(inputurl_num)
init_url = "https://api.twitch.tv/v5/videos/"
url = init_url + str(video_num)+'/comments?'
start = "content_offset_seconds=0"
start_url = url+start

print(start_url)

params = {}
params['client-id'] = "uc4dkdk0aam0pqtmmeujj6ztl5uqmp"  # 내 클라이언트 아이디
params['user-agent'] = ua().chrome
s = requests.session()
my_data = s.get(start_url, headers=params)
json_data = json.loads(my_data.text)
file_name = './' + video_num+'.csv'
file_path = join(current_dir, file_name)
count = 0

while(("_next" in json_data.keys())):

    with open(file_path, 'a') as wf:
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


print("complete!")
