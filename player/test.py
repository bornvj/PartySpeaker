import yt_dlp


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

url='https://youtu.be/68ugkg9RePc?si=BW78VU_r8_fWNkaI'

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        ydl.download([url])
        print("Download completed successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")
