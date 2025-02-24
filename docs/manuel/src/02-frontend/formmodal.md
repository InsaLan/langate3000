# FormModal

Le [composant](composants.md) `FormModal` affiche une boîte de dialogue (ou "modal") qui permet d'afficher ou d'éditer certaines propriétés.

## Attributs

Les attributs d'un FormModal sont les suivants :

```typescript
// Est-ce qu'il faut afficher le modal
open: boolean;

// Titre du modal
title: string;

// Type de boutons du modal
buttons: 'OK' | 'ValiderAnnuler' | 'None';

// Tableau de champs affichés dans le modal
fields: {
  name: string;
  key: string;
  value: string;
  type: string;
  
  // Permet de donner des choix prédéfinis
  choices?: { key: string; value: string }[];
  
  required?: boolean;
}[];

// La fonction qui sera exécutée quand on appuie sur 'OK' ou 'Valider'
function: () => void;
```

Les types d'attributs sont :
- `textarea` : Zone d'entrée de paragraphe;
- `checkbox` : Case à cocher;
- `password` : À ton avis;
- `readonly` : Texte non formaté (police monospace) et non modifiable;
- Tout autre type sera considéré comme une entrée simple.