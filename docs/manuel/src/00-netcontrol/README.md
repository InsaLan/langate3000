# Netcontrol

Netcontrol est le composant de la langate qui interface le backend avec la tête de réseau.

Il permet à la langate de pouvoir effectuer des opérations de plus bas niveau grace à un niveau de privilège plus élevé sur la tête : pour cela, il tourne dans un conteneur ayant la capabilité `NET_ADMIN` et dans le network host.

Netcontrol reçoit ses requêtes par une API REST ([FastAPI](https://fastapi.tiangolo.com/)). Le backend communique avec elle via HTTP.
