# PaginatedTable

`PaginatedTable` est un [composant](composants.md) permettant d'afficher une table d'éléments avec plusieurs pages, de faire des recherches, de trier les résultats et d'effectuer des actions sur les éléments.

Les actions passent par le composant [FormModal](formmodal.md).

## Arguments

Les arguments de création d'une `PaginatedTable` sont les suivants :

```typescript
// La liste des colonnes de la table
properties: {
  name: string;
  key: string;
  ordering: boolean;
  function?: (data: unknown) => string;
}[];

// L'URL de récupération des données sur l'API du backend
url?: string;

data?: { [key: string]: string }[];

// Ces modaux sont présents au dessus de la table et permettent d'y ajouter des éléments
create?: {
  multiple?: (
    (fields: {
      [key: string]: string;
    }[]) => Promise<string | boolean | void>
  );
  modal: {
    title: string;
    buttons: 'OK' | 'ValiderAnnuler' | 'None';
    fields: {
      name: string;
      key: string;
      type: string;
      value?: string;
      choices?: { key: string; value: string }[];
      required?: boolean;
    }[];
  };
  function: (
    (fields: {
      [key: string]: string;
    }) => Promise<string | boolean | void>
  );
};
pagination: boolean;
search: boolean;

// Les actions sont des boutons présents à droite de chaque élément ouvrant des modaux
actions?: { 
  hint: string;
  key: string;
  icon: string;
  modal?: {
    title: string;
    buttons: 'OK' | 'ValiderAnnuler' | 'None';
    
    // additionalUrl n'est pas une propriété de FormModal, elle permet à la PaginatedTable de récupérer des données additionelles à afficher dans un modal (par exemple pour des données qui coûteraient cher à récupérer pour chaque élément)
    additionalUrl?: string;
    
    fields: {
      name: string;
      key: string;
      type: string;
      choices?: { key: string; value: string }[];
      required?: boolean;
    }[] | ((data:unknown) => {
      name: string;
      key: string;
      value: string;
      type: string;
      choices?: { key: string; value: string }[];
      required?: boolean;
    }[]);
  };
  function: (
    (object: { [key: string]: string }) => Promise<string | boolean | void>
  ) | (
    (
      object: { [key: string]: string },
      fields: {
        [key: string]: string;
      }
    ) => Promise<string | boolean | void>
  );
}[];
```