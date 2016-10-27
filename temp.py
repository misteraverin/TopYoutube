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


def main():
    time_str = "2016-10-20T13:06:45.000Z"
    parse_youtube_video(time_str)


def parse_youtube_video(time_str):
    time_str = time_str[:-1]
    parts = re.split('-|\s|\.|:|T', time_str)
    parts = [int(x) for x in parts]
    temp = datetime.datetime(parts[0], parts[1], parts[2], parts[3], parts[4])
    print(strftime("%Y-%m-%d %H:%M UTC", temp.timetuple()))


if __name__ == '__main__':
    main()
