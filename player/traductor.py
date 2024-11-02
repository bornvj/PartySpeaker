import requests
from bs4 import BeautifulSoup

def get_video_title(video_url):
    try:
        r = requests.get(video_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.find("title").text
    except Exception as e:
        return video_url

def write_titles(currentLine):
    i = 0
    with open("soundQueue/queue.txt", 'r') as infile, open('soundQueue/titles.txt', 'w') as outfile:
        for line in infile:
            i += 1
            if i <= currentLine:
                continue
            video_url = line.strip()
            if video_url:
                title = get_video_title(video_url)
                if title:
                    outfile.write(f"{title}\n")
