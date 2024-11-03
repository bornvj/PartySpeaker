import yt_dlp
import time
import os
import glob
import pygame
from traductor import write_titles

ydl_opts_base = {
    'format': 'bestaudio/best',  # Télécharger la meilleure qualité audio
    'extractaudio': True,         # Extraire uniquement l'audio
    'outtmpl': '%(title)s.%(ext)s.audio',  # Nommer le fichier selon le titre de la vidéo
    'enable_file_urls': True,
}

ydl_opts_yt = {
    'format': 'bestaudio/best',  # Télécharger la meilleure qualité audio
    'extractaudio': True,         # Extraire uniquement l'audio
    'audioformat': 'mp3',         # Convertir au format MP3
    'outtmpl': '%(title)s.%(ext)s',  # Nommer le fichier selon le titre de la vidéo
    'postprocessors': [{           # Utiliser un post-processeur pour convertir en MP3
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

file = 'soundQueue/queue.txt'
currentLine = 0
pygame.mixer.init()

garbage_files = glob.glob("*.audio") + glob.glob("*.mp3")
for f in garbage_files:
    os.remove(f)

while True:
    write_titles(currentLine)
    with open(file, 'r') as fichier:
        lines = fichier.readlines()

        count = len(lines)

        if currentLine < count:
            url = lines[currentLine].strip()
            currentLine += 1

            ydl_opts = ydl_opts_yt if "youtube" in url else ydl_opts_base

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([url])
                    audio_files = glob.glob("*.audio") + glob.glob("*.mp3")

                    if len(audio_files) > 0:
                        audio_file = audio_files[0]
                        pygame.mixer.music.load(audio_file)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.Clock().tick(10)
                            write_titles(currentLine)

                        os.remove(audio_file)
                except Exception as e:
                    print(f"Error occurred: {e}")
        else:
            print(".")
            time.sleep(3)
