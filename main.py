__author__ = "Maxim Averin"
# -- coding: utf-8 --

import codecs
import datetime
import requests
import json
import re
import sys
import urllib.request
from datetime import timedelta
from time import strftime
from bs4 import BeautifulSoup

# constants
API_KEY = "AIzaSyAc5hS42qW0TcJ8kGjQct6eIF13teg59VA"
BASE_URL = "https://www.googleapis.com/youtube/v3/search?part=snippet"
BASE_DATA_URL = "https://www.googleapis.com/youtube/v3/videos?part=statistics"
MAX_RESULT = 10
MAX_DISPLAYED = 10
TOTAL_VIDEOS = 10000

current_videos = []
best_commented = []
best_watched = []
best_liked = []


class Video:
    def __init__(self, title, video_id, data, watches=0, comments=0, likes=0):
        self.title = title
        self.id = video_id
        self.data = data
        self.comments = comments
        self.likes = likes
        self.watches = watches

    def __lt__(self, other):
        return (int(self.watches) < int(other.watches)) or \
               ((int(self.watches) == int(other.watches)) and (self.title < other.title))


'''
    @type
    1) insert and sort by comments
    2) insert and sort by likes
    3) insert and sort by watches
'''


def update_information(type, videos):
    html = codecs.open('index.html', 'r', encoding="utf-8")
    soup = BeautifulSoup(html.read(), 'html.parser')

    time = soup.find(class_='time')
    time.string = get_utc_time(get_cur_time())

    # watches = soup.find(class_='titles')
    # watches['class'] = "unvisible"

    need_to_find = ""
    if (type == 1):
        need_to_find = "videos_commented"
    elif (type == 2):
        need_to_find = "videos_liked"
    elif (type == 3):
        need_to_find = "videos_watched"

    tbody_found = soup.find(class_=need_to_find)

    for i, video in enumerate(videos):
        tr = soup.new_tag('tr')
        # id
        th_id = soup.new_tag('th')
        th_id.string = str(i + 1)
        tr.append(th_id)
        # title
        # www.youtube.com/embed/ - good example also
        link_str = "https://youtu.be/" + video.id
        link = soup.new_tag('a', href=link_str)
        # link['class'] = "unvisible"
        link.string = video.title
        th_title = soup.new_tag('th')
        th_title.append(link)
        tr.append(th_title)
        # data
        th_data = soup.new_tag('th')
        th_data.string = video.data
        tr.append(th_data)
        # watches, likes, comments
        th_info = soup.new_tag('th')
        if (type == 1):
            th_info.string = str(video.comments)
        elif (type == 2):
            th_info.string = str(video.likes)
        elif (type == 3):
            th_info.string = str(video.watches)
        tr.append(th_info)
        tbody_found.append(tr)
    html.close()

    output_file = open('index.html', 'w', encoding="utf-8")
    print(soup, file=output_file)
    output_file.close()


def get_cur_time():
    return datetime.datetime.utcnow()


def get_utc_time(current):
    return strftime("%H:%M %Y-%m-%d UTC", current.timetuple())


def convert_youtube_time(current):
    return strftime("%Y-%m-%dT%H:%M:%SZ", current.timetuple())


def parse_youtube_video(time_str):
    time_str = time_str[:-1]
    parts = re.split('-|\s|\.|:|T', time_str)
    parts = [int(x) for x in parts]
    temp = datetime.datetime(parts[0], parts[1], parts[2], parts[3], parts[4])
    return strftime("%Y-%m-%d %H:%M UTC", temp.timetuple())


# parametrs: current time in datetime and delta of timedelta class
def minus_time(current, delta):
    return current - delta

def comment(video):
    return video.comments

def likes(video):
    return video.likes


def get_stats():
    global best_watched, best_liked, best_commented
    ids = ','.join([str(video.id) for video in current_videos])
    GET_QUERY = BASE_DATA_URL + "&id=" + ids + "&key=" + API_KEY
    videos = requests.get(GET_QUERY).json()

    for old_video in current_videos:
        find = old_video.id
        for video in videos['items']:
            if (video['id'] == find):
                watches = int(video['statistics']['viewCount'])
                comments = int(video['statistics']["dislikeCount"])
                likes = int(video['statistics']['likeCount'])
                best_watched.append(Video(old_video.title, old_video.id, old_video.data, watches, comments, likes))
                best_commented.append(Video(old_video.title, old_video.id, old_video.data, watches, comments, likes))
                best_liked.append(Video(old_video.title, old_video.id, old_video.data, watches, comments, likes))
                break
    best_watched.sort(reverse=True)
    best_commented.sort(key=lambda x : int(x.comments), reverse=True)
    best_liked.sort(key=lambda x : int(x.likes), reverse=True)


def get_popular_videos():
    global current_videos
    week_ago = convert_youtube_time(minus_time(get_cur_time(), timedelta(days=7)))
    most_popular = "&chart=mostPopular"
    GET_QUERY = "https://www.googleapis.com/youtube/v3/videos" + "?part=snippet&maxResults=" + str(MAX_RESULT) + \
                most_popular + "&key=" + API_KEY + "&publishedAfter=" + week_ago

    videos = requests.get(GET_QUERY).json()

    for video in videos['items']:
        try:
            title = video['snippet']['title']
            id_video = video['id']
            data = parse_youtube_video(video['snippet']['publishedAt'])
            current_videos.append(Video(title, id_video, data))
        except:
            print(sys.exc_info()[0])
            continue
    get_stats()


def get_videos():
    global current_videos
    current_videos = []
    week_ago = convert_youtube_time(minus_time(get_cur_time(), timedelta(days=7)))
    GET_QUERY = BASE_URL + "&maxResults=" + str(MAX_RESULT) + "&publishedAfter=" + week_ago + "&key=" + API_KEY

    videos = requests.get(GET_QUERY).json()

    for video in videos['items']:
        try:
            title = video['snippet']['title']
            id = video['id']['videoId']
            data = parse_youtube_video(video['snippet']['publishedAt'])
            current_videos.append(Video(title, id, data))
        except:
            continue
    get_stats()


def main():
    global best_watched, best_liked, best_commented
    get_popular_videos()
    get_videos()
    update_information(1, best_commented)
    update_information(2, best_liked)
    update_information(3, best_watched)


if __name__ == '__main__':
    main()
