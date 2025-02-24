# Netcontrol

Netcontrol est le composant de la langate qui interface le backend avec la tête de réseau.

Il permet à la langate de pouvoir effectuer des opérations de plus bas niveau grace à un niveau de privilège plus élevé sur la tête : pour cela, il tourne dans un conteneur ayant la capabilité `NET_ADMIN` et dans le network `host`.

Netcontrol reçoit les requêtes du backend par une [API REST](api.md).

## La nouvelle version

Auparavant, netcontrol était un service systemd, donc pas conteneurisé. Cette nouvelle version est complètement intégrée dans le Docker Compose de la langate.

Netcontrol 2000 utilisait un `ipset` pour faire savoir à la tête quels appareils étaient connectés et quelle [mark](marks.md) leur donner. Des règles `iptables` étaient ensuite ajoutées par [`portail.sh`](https://github.com/InsaLan/scripts-reseau/blob/ifupdown-iptables/portail.sh) La nouvelle version utilise une Map [nftables](nftables.md).

## Autres fonctions

Netcontrol est également utilisé pour d'autres tâches de bas niveau sur la tête de réseau, comme récupérer des informations sur les appareils depuis les baux DHCP et le [SNMP](snmp.md).