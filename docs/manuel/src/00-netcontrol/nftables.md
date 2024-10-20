# nftables

Suite à la mise à jour de la tête de réseau de `iptables` vers `nftables` pour la XIX, netcontrol a été réécrit pour utiliser cet utilitaire.

`nftables` est un utilitaire de gestion des règles réseau qui sert notamment à créer des pare-feux, du NAT, des redirections de ports...

Dans notre cas, on s'en sert pour autoriser la connexion des appareils uniquement si leur utilisateur est connecté à la langate.

À cet effet on utilisait auparavant [ipsets](https://ipset.netfilter.org/), qui nous permettait de garder une collection d'IP ayant accès au réseau et de pouvoir utiliser ça directement dans une règle `iptables`.

La fonctionnalité correspondante sur `nftables` est les [Maps](https://wiki.nftables.org/wiki-nftables/index.php/Maps). Elle nous permet d'associer une adresse MAC à une [mark](marks.md).

## Utiliser nftables à l'intérieur d'un Docker

Netcontrol 2000 n'utilisait pas Docker, c'était un service systemd. Pour la langate3000, on utilise Docker.

Les containers Docker sont par définition isolés de la machine sur laquelle ils tournent. C'est donc compliqué de pouvoir gérer des `nftables` sur la tête de réseau depuis l'intérieur d'un container.

C'est à ça que sert cette ligne dans le `Dockerfile` de netcontrol :
```bash
&& pip install 'git+https://git.netfilter.org/nftables@v1.1.0#egg=nftables&subdirectory=py' \
```

Pour avoir un accès direct à la tête de réseau, il faut également ces lignes dans le docker compose :
```yaml
cap_add:
	- NET_ADMIN
network_mode: "host"
```