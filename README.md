# README Projet IoT Groupe 6 : PartySpeaker

### Description du projet
Ce projet permet de transformer une enceinte en système de lecture audio connecté, capable de jouer des liens YouTube ou des fichiers locaux. Le système inclut un serveur local qui reçoit les liens YouTube, les télécharge et les convertit en format MP3, puis les lit via l'enceinte. Un système de file d'attente gère les liens reçus pour assurer une lecture continue.

### Fonctionnalités
* **Lecture de liens YouTube** : envoie d'un lien YouTube au serveur pour le lire sur l'enceinte.
* **Interface web** : interface simple pour soumettre des liens et contrôler la lecture.
* **Conversion en MP3** : le serveur convertit automatiquement les vidéos YouTube en MP3.
* **Système de file d'attente** : les liens envoyés sont placés dans une file d'attente et lus dans l'ordre.

### Structure du rendu
Voici l'architecture du rendu :

```
.
├── hardware/
│   └── Plan du circuit electronique
├── source/
│   └── PartySpeaker/
│       ├── attack_script/
│       │   ├── README.md
│       │   └── attack_server.sh
│       ├── player/
│       │   ├── player.py
│       │   ├── requirements.txt
│       │   └── traductor.py
│       ├── server/
│       │   ├── source/
│       │   │   ├── index.html
│       │   │   ├── upload.html
│       │   │   └── uploadDone.html
│       │   └── server.c
│       ├── soundQueue/
│       │   ├── queue.txt
│       │   └── titles.txt
│       ├── .gitignore
│       └── Makefile
├── composants.xls
├── README
├── presentation.pdf
├── vulnerabilities.pdf
└── audit/

```

### Prérequis
Hardware : 
* Raspberry Pi ou un ordinateur pour exécuter le serveur
* une enceinte audio

Software :
* Python 3+
* Makefile

### Installation et exécution

1. Installation
```
git clone https://github.com/bornvj/PartySpeaker.git
cd PartySpeaker
cd player
pip install -r requirements.txt
cd ../
make
```
2. Exécution
```
sudo server.bin
```
3. Ouvrir une autre session
```
cd PartySpeaker/
python3 player/player.bin
```

### Utilisation
1. Se connecter au même réseau local que le serveur. (Raspberry Pi ou ordinateur)
2. Ouvrir un navigateur web et aller sur `http://partyspeaker.local/` pour accéder à l'interface web.
3. Cliquer sur "Proposer un son".
![](https://s3.cri.epita.fr/hedgedoc-data.cri.epita.fr/uploads/9ad8e331-d1b7-430f-9c6c-62c4c6aa3551.png)

4. Coller le lien Youtube ou du fichier local.
![](https://s3.cri.epita.fr/hedgedoc-data.cri.epita.fr/uploads/e6dd1295-044a-4417-a47e-d9363848b155.png)

5. Le son sera ajouté à la file d'attente.

### Sécurité et vulnérabilités
Voir vulnerabilities.pdf

### Auteurs
* bornvj
* cryx3001
* Mathieu-CS
* Tsukouille
