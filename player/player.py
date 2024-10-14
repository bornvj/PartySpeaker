import yt_dlp
import time


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

nom_fichier = '../soundQueue/queue.txt'
currentLine = 0
while True:
    with open(nom_fichier, 'r') as fichier:
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
                    print("Download completed successfully.")
                except Exception as e:
                    print(f"Error occurred: {e}")
        else:
            print(".", end = "")
            time.sleep(3)

exit()

url = 'https://youtu.be/68ugkg9RePc?si=BW78VU_r8_fWNkaI'


