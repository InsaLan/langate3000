# Page de gestion

C'est cette page qui permet aux administrateurs de gérer les joueurs et les appareils connectés au réseau. Elle permet de :

- Ajouter / supprimer des utilisateurs;
- Modifier la liste des marks assignées aux appareils ainsi que leurs priorités;
- Modifier la mark d'un appareil donné;
- Whitelist des appareils;
- Kick / Ban des joueurs ou des appareils.

Django dispose d'une page de management native assez capable, mais nous avons choisi d'en faire une custom.

Pour cela, nous avons notamment créé le composant [PaginatedTable](paginatedtable.md).