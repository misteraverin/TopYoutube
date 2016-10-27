__author__ = "Maxim Averin"
# -- coding: utf-8 --

from bs4 import Tag
from bs4 import BeautifulSoup
import urllib.request
import json
import codecs
from time import strftime
import datetime
from datetime import timedelta
import re

# constants
API_KEY = "AIzaSyAc5hS42qW0TcJ8kGjQct6eIF13teg59VA"
BASE_URL = "https://www.googleapis.com/youtube/v3/search?part=snippet"
MAX_RESULT = 10

best_videos = []


class Video:
    def __init__(self, title, id, data, description = "", comments=0, likes=0, watches=0):
        self.title = title
        self.id = id
        self.data = data
        self.description = description
        self.comments = comments
        self.likes = likes
        self.watches = watches

    def debug_print(self):
        print("Data of creation is " + self.title)
        print("Data of creation is " + self.data)
        print("Number of comments is " + repr(self.comments))


def update_information():
    html = codecs.open('index.html', 'r', encoding="utf-8")
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html.read(), 'html.parser')

    tbody_found = soup.find(class_='videos')
    for i, video in enumerate(best_videos):
        tr = soup.new_tag('tr')
        # id
        th_id = soup.new_tag('th')
        th_id.string = str(i + 1)
        tr.append(th_id)
        # title
        th_title = soup.new_tag('th')
        th_title.string = video.title
        tr.append(th_title)
        # data
        th_data = soup.new_tag('th')
        th_data.string = video.data
        tr.append(th_data)
        # link
        th_link = soup.new_tag('th')
        # www.youtube.com/embed/ - good example also
        link_str = "https://youtu.be/" + video.id
        link = soup.new_tag('a', href = link_str)
        link.string = "watch"
        th_link.append(link)
        tr.append(th_link)
        tbody_found.append(tr)
    html.close()

    output_file = open('index2.html', 'w', encoding="utf-8")
    print(soup, file=output_file)
    output_file.close()


def get_cur_time():
    return datetime.datetime.utcnow()


def convert_youtube_time(current):
    return strftime("%Y-%m-%dT%H:%M:%SZ", current.timetuple())


def parse_youtube_video(time_str):
    time_str = time_str[:-1]
    parts = re.split('-|\s|\.|:|T', time_str)
    parts = [int(x) for x in parts]
    temp = datetime.datetime(parts[0], parts[1], parts[2], parts[3], parts[4])
    return strftime("%Y-%m-%d %H:%M UTC", temp.timetuple())
    #return strftime("%Y-%m-%d %H:%M UTC", temp)



# parametrs: current time in datetime and delta of timedelta class
def minus_time(current, delta):
    return current - delta


def get_videos():
    now = convert_youtube_time(get_cur_time())
    week_ago = convert_youtube_time(minus_time(get_cur_time(), timedelta(days=7)))
    GET_QUERY = BASE_URL + "&maxResults=" + str(MAX_RESULT) + "&publishedAfter=" + week_ago + "&key=" + API_KEY
    request = urllib.request.urlopen(GET_QUERY)

    #parse_youtube_video("2016-10-20T13:06:45.000Z")

    videos = json.loads(request.read().decode(request.info().get_param('charset') or 'utf-8'))
    count = 0
    for video in videos['items']:
        try:
            count += 1
            title = video['snippet']['title']
            id = video['id']['videoId']
            data = parse_youtube_video(video['snippet']['publishedAt'])
            best_videos.append(Video(title, id, data))
        except:
            continue


def main():
    get_videos()
    update_information()


if __name__ == '__main__':
    main()
