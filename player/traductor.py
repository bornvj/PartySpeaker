from pytube import YouTube

def get_video_title(video_url):
    try:
        yt = YouTube(video_url)
        return yt.title
    except Exception as e:
        return None


with open("soundQueue/queue.txt", 'r') as infile, open('soundQueue/titles.txt', 'w') as outfile:
    for line in infile:
        video_url = line.strip()
        if video_url:
            title = get_video_title(video_url)
            if title:
                outfile.write(f"{title}\n")