# Backend

Le backend de la langate est écrit en Python et utilise [DRF](django-rest-framework.org).

## Configuration

### LAN mode

La variable d'envionnement `LAN` permet de définir si la gate est démarré pour l'event principal ou pour une mini.
- Si la variable est à 1, lors du login d'un utilisateur, la gate va vérifier si l'utilisateur existe
sur le site de l'insalan et si l'utilisateur n'existe pas en local, un compte sera créé pour lui.
- Si la variable est à 0, il sera nécessaire de créer manuellement les utilisateurs dans la base de données.

Le processus complet de login est détaillé dans la section [Vues](vues.md#users).
