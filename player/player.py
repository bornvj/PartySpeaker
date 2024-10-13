#!/bin/python3

import os
import time
import pygame

dossier = '../soundQueue/'

pygame.mixer.init()

while True:
    mp3_files = [f for f in os.listdir(dossier) if f.endswith('.mp3')]
    
    while not mp3_files or len(mp3_files) == 0:
        print("Aucun fichier MP3 à jouer")
        time.sleep(3)


    oldest_file = min(mp3_files, key=lambda f: os.path.getctime(os.path.join(dossier, f)))
    oldest_file_path = os.path.join(dossier, oldest_file)

    print(f'Joue: {oldest_file_path}')
    pygame.mixer.music.load(oldest_file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(1)

    os.remove(oldest_file_path)
    print(f'Supprimé: {oldest_file_path}')

# Quitter pygame
pygame.mixer.quit()