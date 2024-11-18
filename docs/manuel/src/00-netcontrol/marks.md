# Marks

Les marks sont des numéros utilisés par une [`ip rule`](https://github.com/InsaLan/scripts-reseau/blob/main/ip_rules.sh) pour déterminer quelle route vers internet doit emprunter le traffic d'un appareil. Une route (définie dans `/etc/iproute2/rt_tables` et remplie par [`autoroute_aec`](https://github.com/InsaLan/scripts-reseau/blob/main/autoroute_aec.py)) est associée à un tunnel, qui est la représentation d'un VPN sur la tête.

On utilise typiquement :
- 100 pour le traffic sortant directement par la DSI
- 101 pour le traffic sortant par le VPN1
- 102 pour le traffic sortant par le VPN2
- . . .
- 1000 pour le traffic sortant par Quantic (LAN uniquement)