# Netcontrol

Netcontrol est le composant de la langate qui interface le backend avec la tête de réseau.

Il permet à la langate de pouvoir effectuer des opérations de plus bas niveau grace à un niveau de privilège plus élevé sur la tête.

Il communique via sockets UNIX. Les informations sont précédées d'une annonce de leur taille, sous la forme d'un int de 4 octets. Les informations en elles-mêmes sont toujours des dictionnaires Python encodés en [pickle](https://docs.python.org/3/library/pickle.html).
