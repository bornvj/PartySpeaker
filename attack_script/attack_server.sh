#!/bin/bash

# Vérifie si un chemin de fichier a été fourni en argument
if [[ -z "$1" ]]; then
    echo "Usage : $0 <chemin_vers_fichier.mp3>"
    exit 1
fi

MP3_FILE="$1"

# Vérifie si le fichier MP3 existe
if [[ ! -f "$MP3_FILE" ]]; then
    echo "Erreur : Le fichier $MP3_FILE n'existe pas."
    exit 1
fi

# Dossier contenant le fichier MP3
DIR_PATH=$(dirname "$MP3_FILE")
FILE_NAME=$(basename "$MP3_FILE")

# Obtient l'adresse IP de la machine
IP_ADDRESS=$(hostname -I | awk '{print $1}')

# Change de répertoire pour démarrer le serveur dans le dossier du fichier
cd "$DIR_PATH" || exit 1

# Démarre un serveur HTTP en arrière-plan
echo "Lancement du serveur HTTP local sur http://$IP_ADDRESS:8080"
python3 -m http.server 8080 &

# Attend une seconde pour s'assurer que le serveur est bien lancé
sleep 1

# URL complète du fichier .mp3
FILE_URL="http://$IP_ADDRESS:8080/$FILE_NAME"

# Envoie une requête POST à raspberrypi.local avec l'URL du fichier
echo "Envoi de l'URL du fichier MP3 à http://raspberrypi.local/upload"
curl -X POST -d "text=$FILE_URL" http://raspberrypi.local/upload

# Message de confirmation
echo "Requête envoyée avec succès : $FILE_URL"
