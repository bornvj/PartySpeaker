# Serveur HTTP pour Partage de Fichiers MP3

Ce projet fournit un script Bash qui lance un serveur HTTP en local pour exposer un fichier `.mp3`. Il inclut également une requête POST envoyée à un serveur distant, `http://raspberrypi.local/upload`, avec l'URL du fichier `.mp3` partagé. Ce projet peut être utilisé pour tester le téléchargement de fichiers audio depuis une source externe.

## Prérequis

- **Python 3** : nécessaire pour lancer le serveur HTTP.
- **curl** : pour envoyer la requête POST au serveur distant.

## Utilisation

1. **Rendre le script exécutable** :

   ```bash
   chmod +x serveur_mp3.sh
   ```

## Fonctionnement du Script

Le script `serveur_mp3.sh` est conçu pour partager un fichier `.mp3` via un serveur HTTP local et envoyer son URL à un serveur distant. Voici le déroulement de ses opérations :

1. **Vérification des Arguments** : Le script commence par vérifier qu'un chemin de fichier `.mp3` a bien été fourni en argument. Si aucun chemin n'est fourni, il affiche un message d'utilisation et s'arrête.

2. **Vérification du Fichier** : Il vérifie ensuite l'existence du fichier `.mp3` spécifié. Si le fichier n'est pas trouvé, le script affiche une erreur et s'arrête.

3. **Lancement du Serveur HTTP** : Le script utilise `python3 -m http.server 8080` pour lancer un serveur HTTP en local sur le port 8080, en exposant le répertoire contenant le fichier `.mp3`. Cela permet à tout appareil connecté au réseau local d’accéder et de télécharger le fichier en utilisant l'URL `http://<IP_de_la_machine>:8080/nom_du_fichier.mp3`.

4. **Envoi de l'URL du Fichier** : Une fois le serveur démarré, le script récupère l'adresse IP locale de la machine et génère l'URL complète du fichier. Il utilise ensuite `curl` pour envoyer une requête POST à `http://raspberrypi.local/upload` avec l'URL du fichier en paramètre `text`.

5. **Téléchargement** : Le fichier `.mp3` est alors accessible depuis n'importe quel appareil du réseau en accédant à l'URL fournie. Le script continue à exécuter le serveur HTTP jusqu'à ce qu'il soit arrêté manuellement.

Ce script est particulièrement utile pour tester la récupération de fichiers depuis un serveur externe, en simulant un environnement de téléchargement de fichier `.mp3` dans un réseau local.

## Exemple d'Attaque : Dépassement de Mémoire avec un Fichier `.mp3` Volumineux

Dans le cadre de tests de sécurité, il est possible d’exploiter la taille du fichier `.mp3` pour causer des problèmes de performance ou des plantages sur des systèmes limités en mémoire, comme un Raspberry Pi. En envoyant un fichier `.mp3` d'une taille supérieure à la mémoire disponible sur le Raspberry Pi, le système pourrait être incapable de charger ou de traiter correctement le fichier. Cela peut entraîner un ralentissement significatif, un arrêt de services, ou même un crash du système, en fonction de la manière dont il gère les ressources insuffisantes. Ce type d'attaque met en évidence l'importance de contrôler la taille des fichiers et d'utiliser des mécanismes de limitation pour éviter les dépassements de mémoire sur des systèmes embarqués.

