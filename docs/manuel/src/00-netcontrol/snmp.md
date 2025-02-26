# SNMP

Le SNMP (Simple Network Management Protocol) est un protocole réseau qui nous permet notamment de recueillir des **stats sur les switchs**, et ici, trouver quel appareil est connecté sur quel switch. Cette fonctionnalité est utile par exemple pour retrouver un joueur qui fait une MàJ de 120 Go et aller lui parler poliment.

Les données sont rassemblées dans une **communauté** SNMP, qu'on définit dans la variable d'environnement `SNMP_COMMUNITY`, et qui aux dernières nouvelles était pour nous `hotlinemontreal`.

## En Python

On a une classe `Snmp` qui utilise la librairie [`puresnmp`](https://puresnmp.readthedocs.io/en/latest/index.html) pour faire **des requêtes sur tous les switchs** jusqu'à en trouver un qui a la bonne adresse MAC branchée dessus. La liste de switchs lui est fournie par la classe `Devices`, qui les retrouve en prenant toutes les IPs entre `172.16.1.20` et `172.16.1.199` dans le fichier `/etc/hosts` de la tête de réseau.

Les switchs ne savent pas si les macs qu'ils connaissent sont branchées directement ou derrière d'autres switchs. On s'assure donc que la mac est seule sur le port pour garantir qu'il n'y a pas de switch entre les deux.

Un OID est **l'identifiant d'un morceau de données** en SNMP. Notre requête utilise l'OID `1.3.6.1.2.1.17.4.3.1.2` (oui c'est limpide comme codage). Je laisse ChatGPT expliquer :

```
Each nyumbew in da OID has a speshaw meaning! ⸜(｡˃ ᵕ ˂ )⸝💖

1️⃣ 1.3 – Dis is fow da ISO (Intewnationaw Owganization fow Standawdization)! So fancy~ (⁄ ⁄>⁄ω⁄<⁄ ⁄)✨

2️⃣ 1.3.6 – OwO! Dis means it fowwows da DOD (Depawtment of Defense) standawds~ (´꒳`) (Did u knyow? SNMP comes fwom da ancient ARPANET times! UwU so histowic~)

3️⃣ 1.3.6.1 – Hewwo IANA (Intewnyet Assigned Nyumbews Authowity)!! (*≧ω≦)🎉

4️⃣ 1.3.6.1.2 – Ooooh, dis means it’s fow managing infowmation, wike nyetwork deviceys! (๑>◡<๑)✨

5️⃣ 1.3.6.1.2.1 – Dis pointies to da MIB-2 (Management Infowmation Base)! A big wittwe wibwawy of nyetwowk data~ 📚🐾

6️⃣ 1.3.6.1.2.1.17 – Ooh! Dis is fow da Bwidge MIB, which handwes switchies & MAC addwess tabwies! (✿◕‿◕)💡

7️⃣ 1.3.6.1.2.1.17.4.3.1.2 – (✧ω✧) OH MAI! Dis is da MAC addwess tabwe, which maps MACs to switchie powts! UwU💻✨

B-basically, each step goes deeper into da OID twee, getting mowe specific untiw u find da exact data u wan~! ✨(∩˃o˂∩)✨💖 Hope dis hewps!!
```

J'espère que c'est plus clair.

## Débit sur un port

Pour déterminer la bande passante utilisée par un port spécifique, on peut utiliser ces OIDs :

- `1.3.6.1.2.1.31.1.1.1.6` ou `ifHCInOctets`, le nombre d'octets téléchargés;
- `1.3.6.1.2.1.31.1.1.1.10` ou `ifHCOutOctets`, le nombre d'octets envoyés.

Ces OIDs donnent un nombre absolu d'octets à un moment donné, il faut donc les **mesurer à deux instants** et diviser par l'intervalle pour trouver le débit. D'après mes tests, l'intervalle de mise à jour des données est au moins de 2.5 secondes, mais ça pourrait varier selon le switch.

## MIBs

Les OIDs peuvent êtres retrouvés dans des MIBs, qui sont les **fichiers de référence** du SNMP. Ces MIBs contiennent les OIDs associés à des noms descriptifs comme `IF-MIB::ifXTable`.

Notre bibliothèque Python, [`puresnmp`](https://puresnmp.readthedocs.io/en/latest/index.html) a pour but **de ne pas utiliser de MIBs**, qui compliquent un peu la vie car c'est des fichiers à gérer en plus. On localise donc les OIDs qu'on voudra utiliser et on s'en sert dans le script.

Pour explorer des MIBs, [cet outil](https://cric.grenoble.cnrs.fr/Administrateurs/Outils/MIBS/?oid=1) du CNRS est très utile. Sinon, on peut aussi trouver des applications comme [MIB Browser](https://ireasoning.com/mibbrowser.shtml) qui sont souvent fournies avec des sélections de MIBs.
