# Metrics

Afin d'exposer des métriques à l'extérieur et ainsi pouvoir les afficher dans un beau Grafana, on intègre la librairie [prometheus-client](https://pypi.org/project/prometheus-client/).

Les métriques exposées sont :
- `langate_connected_devices` : cette jauge compte le nombre d'appareils connectés par mark.
- `langate_users_total/created` : il s'agit d'un compteur du nombre d'utilisateurs créés. La métrique `langate_users_total` est celle qui nous intéresse, tandis que `langate_users_created` est créé automatiquement et contient la date de dernière modification.

Ces métriques sont exposées sous le format [prometheus](https://prometheus.io/docs/instrumenting/exposition_formats/#text-based-format) via l'endpoint `api.<website_host>/network/metrics`.

Voici un exemple de sortie de cet endpoint :
```py
# HELP langate_connected_devices Amount of connected devices
# TYPE langate_connected_devices gauge
langate_connected_devices{mark="100"} 0.0
langate_connected_devices{mark="101"} 1.0
# HELP langate_users_total Total amount of users registered.
# TYPE langate_users_total counter
langate_users_total 2.0
# HELP langate_users_created Total amount of users registered.
# TYPE langate_users_created gauge
langate_users_created 1.740489891358599e+09
```
