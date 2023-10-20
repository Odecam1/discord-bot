# Code du Bot Discord

Ce code est un exemple d'un bot Discord créé avec la bibliothèque discord.py, qui est conçu pour être utilisé sur un serveur Discord. Le bot effectue plusieurs tâches, telles que le salut des nouveaux membres, la gestion de mots interdits dans les messages, l'affichage d'informations sur le serveur, la création de sondages et la possibilité pour les modérateurs de gérer une liste de mots interdits et de bannir des utilisateurs.

## Configuration du bot

Le code commence par l'importation des bibliothèques nécessaires, la définition de variables, telles que `channel_id` et `token`, et la définition de fonctions pour sauvegarder et charger la liste des mots interdits depuis un fichier JSON.

## Chargement des mots interdits

Le code charge initialement la liste des mots interdits à partir du fichier "banned_words.json" ou crée une nouvelle liste vide si le fichier n'existe pas.

## Initialisation du bot Discord

Le bot Discord est configuré avec des intentions (intents) pour gérer les événements, tels que les arrivées de nouveaux membres et les messages. Le préfixe des commandes est défini comme "!".

## Gestion des événements

Plusieurs événements sont gérés par le bot, notamment :

- `on_ready` : Ce message est affiché lorsque le bot est prêt à fonctionner.
- `on_member_join` : Le bot accueille les nouveaux membres du serveur dans un canal de texte.
- `on_message` : Le bot vérifie les messages pour la présence de mots interdits et les supprime si nécessaire.

## Définition des commandes

Plusieurs commandes sont définies pour permettre aux utilisateurs de contrôler le bot, notamment :

- `!stats` : Affiche des informations sur le serveur, telles que le nombre de membres, de bots, de membres en ligne et de canaux.
- `!créer_sond` : Permet de créer un sondage avec une question et des options.
- `!ajouter_mot_interdit` : Permet aux modérateurs d'ajouter des mots interdits à la liste.
- `!liste_mots_interdits` : Affiche la liste des mots interdits.
- `!supprimer_mot_interdit` : Permet aux modérateurs de supprimer des mots de la liste interdite.
- `!bannisement_membre` : Permet aux modérateurs de bannir des utilisateurs.

## Démarrage du bot

La dernière ligne du code `bot.run(token)` lance le bot Discord en utilisant le token spécifié.

Ce bot réagit aux événements sur le serveur et exécute des commandes spécifiques en fonction des actions des utilisateurs. Il peut également effectuer une modération de base en supprimant les messages contenant des mots interdits et en permettant aux modérateurs de gérer la liste des mots interdits et de bannir des utilisateurs.

