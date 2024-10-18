import yt_dlp
import time
import os
import glob
import pygame
import subprocess

ydl_opts = {
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

while True:
    subprocess.run(['python3', 'player/traductor.py']) # run a traductor
    os.environ['LINECOUNT'] = str(currentLine)
    with open(file, 'r') as fichier:
        # Lire toutes les lignes dans une liste
        lines = fichier.readlines()
        
        count = len(lines)

        # Vérifier si currentLine est dans la plage
        if currentLine < count:
            # Afficher la ligne actuelle
            url = lines[currentLine].strip()
            currentLine += 1

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([url])
                    mp3_files = glob.glob("*.mp3")

                    if len(mp3_files) == 1:
                        mp3_file = mp3_files[0]
                        pygame.mixer.music.load(mp3_file)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.Clock().tick(10)

                        os.remove(mp3_file)
                except Exception as e:
                    print(f"Error occurred: {e}")

                # TODO: play the file and delete the file
                # TODO: get the name of the song for the website instead of the link
                # TODO: send the C server the info of the current line status to avoid printing already played song
        else:
            print(".", end = "\n")
            time.sleep(3)

exit()

url = 'https://youtu.be/68ugkg9RePc?si=BW78VU_r8_fWNkaI'


