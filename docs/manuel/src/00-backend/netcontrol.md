# Netcontrol

Netcontrol est le composant de la langate qui interface le backend avec la tête de réseau.

Il permet à la langate de pouvoir effectuer des opérations de plus bas niveau grace à un niveau de privilège plus élevé sur la tête.

Le backend communique via des requêtes HTTP à l'API REST ([FastAPI](https://fastapi.tiangolo.com/)) du module netcontrol de la langate. L'adresse utilisée pour les requêtes est la route par défaut du docker du backend, sur laquelle est bind l'API.

Pour effectuer ces requêtes, le backend dispose d'une classe Netcontrol, dans `langate/modules/netcontrol.py`, instanciée dans `langate/settings.py`. C'est cette instance qu'on utilise pour faire les requêtes, en l'important là où il y en a besoin. La classe Netcontrol possède une méthode par requête possible, avec les arguments spécifiques à chacune d'entre elles.

## Faire les requêtes manuellement

On peut utiliser `curl` pour simuler les requêtes au netcontrol depuis la tête de réseau en faisant attention au type de la requête (`GET`, `POST`, `DELETE` ou `PUT`). 
Les requêtes se font ainsi : `curl -X {Type} http://{IP}:6784/{Arguments}` où :
- `{Type}` est le type de la requête,
- `{IP}` l'ip sur l'interface `docker0`,
- `{Arguments}` les arguments sous la forme `endpoint?arg1=..&arg2=..&arg3=...` ou `endpoint` s'il n'y a pas d'argument. 