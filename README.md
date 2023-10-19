# Bot Discord Multifonction

## Description

Il s'agit d'un bot Discord multifonctionnel qui offre diverses fonctionnalités utiles aux membres du serveur.

## Fonctionnalités

1. **Salutations** : Lorsqu'un nouvel utilisateur rejoint le serveur, le bot envoie un message de bienvenue dans un canal spécifique.
2. **Informations sur le serveur** : Les utilisateurs peuvent demander des informations sur le serveur, telles que le nombre total de membres, les membres en ligne et les canaux.
3. **Gestion des sondages** : Les utilisateurs peuvent créer des sondages simples où d'autres membres peuvent voter en utilisant des réactions.
4. **Convertisseur de devises** : Les utilisateurs peuvent convertir un montant d'une devise à une autre.
5. **Modération** : Le bot peut détecter automatiquement et supprimer les messages contenant des mots interdits. Les modérateurs du serveur peuvent également demander de bannir ou de mettre en sourdine un utilisateur spécifique.
6. **Pierre-papier-ciseaux (Chifoumi)** : Les utilisateurs peuvent jouer à un jeu de pierre-papier-ciseaux contre le bot.

## Prérequis

- [Python](https://www.python.org/) 3.7+
- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- Un jeton (token) pour un bot Discord

## Utilisation

1. Clonez ce dépôt.
2. Modifiez les variables `channel_id` et `token` dans le code avec vos valeurs spécifiques.
3. Exécutez le bot avec `python main.py.py`.

## Commandes

- `!stats` : Obtenez des statistiques sur le serveur.
- `!créer_sond` : Créez un sondage. Utilisation : `!créer_sond "Question" Option1 Option2 ...`
- `!ajouter_mot_interdit` : Ajoutez un mot interdit à la liste (réservé aux modérateurs). Utilisation : `!ajouter_mot_interdit mot`
- `!liste_mots_interdits` : Liste tous les mots interdits.
- `!supprimer_mot_interdit` : Supprime un mot interdit de la liste (réservé aux modérateurs). Utilisation : `!supprimer_mot_interdit mot`

## Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.
