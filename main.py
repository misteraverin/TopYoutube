__author__ = "Maxim Averin"
# -- coding: utf-8 --

from bs4 import Tag
from bs4 import BeautifulSoup
import urllib.request
import json

# constants
API_KEY = "AIzaSyAc5hS42qW0TcJ8kGjQct6eIF13teg59VA"
BASE_URL = "https://www.googleapis.com/youtube/v3/search?part=snippet"
MAX_RESULT = 10

best_videos = []


class Video:
    def __init__(self, title, data, description, comments=0, likes=0, watches=0):
        self.title = title
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
    html = open('index.html', 'r', encoding="utf-8")
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    tbody_found = soup.find(class_='videos')
    for i, video in enumerate(best_videos):
        tr = soup.new_tag('tr')
        #id
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
        # description
        th_description = soup.new_tag('th')
        th_description.string = video.description
        tr.append(th_description)
        tbody_found.append(tr)
    html.close()

    output_file = open('index2.html', 'w')
    print(soup.prettify('latin-1').decode('utf-8'), file=output_file)
    output_file.close()


def get_videos():
    time = "2016-10-26T00:00:00Z"
    GET_QUERY = BASE_URL + "&maxResults=" + str(MAX_RESULT) + "&publishedAfter=" + time + "&key=" + API_KEY
    request = urllib.request.urlopen(GET_QUERY)

    videos = json.loads(request.read().decode(request.info().get_param('charset') or 'utf-8'))
    count = 0
    for video in videos['items']:
        try:
            count += 1
            best_videos.append(Video(video['snippet']['title'], video['id']['videoId'], video['snippet']['publishedAt']))
            print("New video №", count)
            print("Video ID: ", video['id']['videoId'])
            print("Video Title: ", video['snippet']['title'])
            print("Data: ", video['snippet']['publishedAt'])
        except:
            continue


def main():
    get_videos()
    update_information()


if __name__ == '__main__':
    main()
