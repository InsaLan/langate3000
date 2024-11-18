# Classe netcontrol

Le backend communique via des requêtes HTTP à l'[API REST](../00-netcontrol/api.md) du module netcontrol de la langate. L'adresse utilisée pour les requêtes est la route par défaut du docker du backend, sur laquelle est bind l'API.

Pour effectuer ces requêtes, le backend dispose d'une classe Netcontrol, dans `langate/modules/netcontrol.py`, instanciée dans `langate/settings.py`. C'est cette instance qu'on utilise pour faire les requêtes, en l'important là où il y en a besoin. La classe Netcontrol possède une méthode par requête possible, avec les arguments spécifiques à chacune d'entre elles.