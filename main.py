__author__ = "Maxim Averin"

from bs4 import Tag
from bs4 import BeautifulSoup

#constants
API_KEY = "AIzaSyAc5hS42qW0TcJ8kGjQct6eIF13teg59VA"

class Video:
    def __init__(self, title, data, comments=0, likes=0, watches=0):
        self.title = title
        self.data = data
        self.comments = comments
        self.likes = likes
        self.watches = watches

    def debug_print(self):
        print("Data of creation is " + self.title)
        print("Data of creation is " + self.data)
        print("Number of comments is " + repr(self.comments))


def update_information():
    html = open('index1.html', 'r', encoding="utf-8")
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a'):
        a.string.replace_with("Alice!")
    html.close()

    output_file = open('index2.html', 'w')
    print(soup.prettify(), file=output_file)
    output_file.close()



def main():
    # first_video = Video("Cool video, dude!", "22.06")
    #  first_video.debug_print()
    update_information()


if __name__ == '__main__':
    main()
