__author__ = "Maxim Averin"
# -- coding: utf-8 --

import codecs
import datetime
import requests
import json
import re
import sys
from datetime import timedelta
from time import strftime
from bs4 import BeautifulSoup
import config

# constants

BASE_URL = "https://www.googleapis.com/youtube/v3/search?part=snippet"
BASE_DATA_URL = "https://www.googleapis.com/youtube/v3/videos?part=statistics"
MAX_RESULT = 50
MAX_DISPLAYED = 10
TOTAL_VIDEOS = 300

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




def get_videos():
    global current_videos
    current_videos = []
    week_ago = convert_youtube_time(minus_time(get_cur_time(), timedelta(days=7)))
    GET_QUERY_BASE = BASE_URL + "&maxResults=" + str(
                    MAX_RESULT) + "&publishedAfter=" + week_ago + "&key=" + config.API_KEY

    count_videos = 0
    times = 0
    next_page_token = False
    page_token = 0
    while (count_videos <= TOTAL_VIDEOS):
        try:
            print("NEW TIME", times)
            print(page_token)
            times += 1
            if(next_page_token == False):
                GET_QUERY = GET_QUERY_BASE
                next_page_token = True
            else:
                GET_QUERY = GET_QUERY_BASE + "&pageToken=" + page_token
            videos = requests.get(GET_QUERY).json()
            page_token = videos['nextPageToken']
            for video in videos['items']:
                try:
                    title = video['snippet']['title']
                    id = video['id']['videoId']
                    data = parse_youtube_video(video['snippet']['publishedAt'])
                    current_videos.append(Video(title, id, data))
                except:
                    continue
            count_videos += 50
        except:
            continue
    #get_stats(0)


def main():
    global best_watched, best_liked, best_commented
    with open('template.html', mode='r', encoding='utf-8') as input:
        with open('index.html', mode='w') as output:
            for line in input:
                output.write(line)
    get_videos()


if __name__ == '__main__':
    main()
