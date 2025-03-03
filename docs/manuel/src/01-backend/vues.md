# Vues

Pour comprendre la structure d'une vue Django, il est conseillé de lire la
[documentation du
site](https://docs.insalan.fr/backend/02-structure/applications/vues.html).

Tout les endpoints ne seront pas détaillés ici, seulement les plus importants ou
ceux qui nécessitent une explication particulière.

## Users

Les vues "utilisateurs" sont les fonctions éxécutées à la réception d'une
requête relative à la gestion ou l'authentification d'un utilisateur. Ces vues
sont définies dans le fichier `views.py` de l'application `users`.

### Login

Pour la connexion d'un utilisateur, le login standard de Django a été modifié
afin de rajouter la création de compte automatique depuis le site.

Le processus de connexion est le suivant :
1. L'utilisateur envoie un POST à `/users/login/` avec les champs `username` et
   `password`.
2. Si l'utilisateur n'existe pas dans la base de données : 2.1. On envoie une
    requête au site de l'insalan pour récupérer les informations de
    l'utilisateur. 2.2. Si l'utilisateur n'existe pas sur le site de l'insalan,
    la gate reçoit une erreur 404 et cette erreur est renvoyée à l'utilisateur.
    2.3. Si l'utilisateur existe sur le site de l'insalan, on crée un compte
    pour lui dans la base de données de la gate.
3. On vérifie les identifiants de l'utilisateur.
4. On utilise le `login` de Django pour connecter l'utilisateur.

Ce processus peut être modifié en fonction de l'état de la variable
d'environnement `LAN`. Si la variable est à 0, l'étape 2 est ignorée et
l'utilisateur doit être créé manuellement dans la base de données.

## Network

Les vues "réseau" sont les fonctions éxécutées à la réception d'une requête
relative à la gestion des appareils connectés et du réseau. Ces vues sont
définies dans le fichier `views.py` de l'application `network`.

Ces vues sont protégées et nécessitent d'être authentifié en tant
qu'administrateur pour être utilisées.

Les vues de l'application `network` ne sont pas très complexes de la gate et ont
pour but de renvoyer les listes d'appareils connectés, d'appareils
whitelistés,... de manière paginée. Certains endpoints permettent aussi d'avoir
des informations sur un appareil en particulier ou de le modifier.
