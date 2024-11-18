# API REST

Netcontrol est une API REST comme le backend, mais il n'utilise pas Django. Il utilise [FastAPI](https://fastapi.tiangolo.com/).

## Endpoints

On interface avec l'API en faisant des requêtes HTTP sur la bonne adresse, ou **endpoint**. Il y en a un pour chaque méthode publique de netcontrol. Ces endpoints peuvent prendre des paramètres (heureusement, sinon ils ne serviraient pas à grand chose).

On définit un endpoint dans main.py comme ceci :

```python
@app.post("/connect_user")
def connect_user(mac: str, mark: int, name: str):
    return nft.connect_user(mac, mark, name)
```

Les paramètres passés dans l'adresse seront automatiquement convertis en arguments Python utilisables dans le code.

## Faire les requêtes manuellement

On peut utiliser `curl` pour simuler les requêtes au netcontrol depuis la tête de réseau en faisant attention au type de la requête (`GET`, `POST`, `DELETE` ou `PUT`). 
Les requêtes se font ainsi : 
```bash
curl -X {Type} http://{IP}:6784/{Arguments}
```
Où :
- `{Type}` est le type de la requête,
- `{IP}` l'ip sur l'interface `docker0`,
- `{Arguments}` les arguments sous la forme `endpoint?arg1=..&arg2=..&arg3=...` ou `endpoint` s'il n'y a pas d'argument. 