# Traductions

Le backend contient de nombreux messages, notamment des messages d'erreur, qui sont écrits en anglais et ont besoin d'être traduits en français pour rester cohérents avec le front (où ils peuvent apparaître sous forme de notifications).

Pour cela, on utilise la fonctionnalité i18n de Django qui permet de traduire tous les messages dans plusieurs langages. Ces traductions sont compilées à chaque lancement de la Langate dans un format binaire plus efficace. Ensuite, le middleware `django.middleware.locale.LocaleMiddleware` définit la langue automatiquement grace aux headers des requêtes faites sur le back.

Cette page est relativement longue, mais **les seules parties nécessaires si tout est déjà setup sont [Écrire un message](#écrire-un-message), [Générer le fichier de traductions](#générer-le-fichier-de-traductions) et [Traduire les messages](#traduire-les-messages).**

## Déclaration des langues dans `settings.py`

Comme toutes les fonctionnalités Django, les traductions sont paramétrées dans le fichier `langate/setting.py`. Dans ce fichier :
- On déclare le middleware `django.middleware.locale.LocaleMiddleware` dans `MIDDLEWARE` (attention, il faut le mettre après `SessionMiddleware` et avant `CommonMiddleware` dans la liste)
- On active la fonctionnalité de traduction :
```python
USE_I18N = True
```
- On définit la langue par défaut :
```python
LANGUAGE_CODE = 'en'
```
- On déclare les langages qu'on utilise :
```python
LANGUAGES = [
    ("en", _("English")),
    ("fr", _("French")),
]
```
- On définit les chemins des fichiers de traduction :
```python
LOCALE_PATH='locale'
LOCALE_PATHS = [path.join(BASE_DIR, 'locale')]
```

## Écrire un message

Pour écrire un `string` qui changera en fonction de la langue, on utilise `django.utils.translation.gettext_lazy()`. Vue la fréquence d'utilisation de cette fonction, on va l'importer sous le nom `_()`. Ensuite, plus qu'à lui passer un `string` en argument, et on pourra le traduire.

## Générer le fichier de traductions

Les traductions sont définies dans le fichier `locale/[code de langue]/LC_MESSAGES/django.po`. Pour générer ce fichier avec tous les messages du backend, il faut lancer le docker compose et rentrer dans le docker du backend :
```sh
docker compose -f docker-compose-beta.yml up --build -d
docker exec -it infra-langate-beta-backend-1 sh
```
Une fois qu'on est là, on peut utiliser le script `manage.py` pour lancer la bonne commande Django :
```sh
python manage.py makemessages -a
```
**Attention :** si le fichier `django.po` n'existe pas déjà, il faudra probablement le créer à la main avant.

## Traduire les messages

Pour traduire les messages, on ouvre le fichier `django.po` dans notre éditeur de texte préféré. Dedans, on retrouve tous les messages qui ont été écrits avec `_()` dans les champs `msgid`; il faut écrire les traductions correspondantes dans les champs `msgstr`.

En commentaire avant chaque entrée, on retrouve les **emplacements d'occurences** du message dans nos fichiers.

Si un nouveau message a été ajouté, et un message un peu similaire avait déjà été traduit avant, on peut aussi retrouver le `msgid` correspondant. Dans ce cas, la traduction a été **automatiquement remplie** et il faudra la changer car elle est très rarement bonne.

Exemple :
```
#: langate/network/models.py:186 langate/network/views.py:315
#, fuzzy
#| msgid "Invalid data format"
msgid "Invalid mark"
msgstr "Format de données invalide"
```

Ici, on voit que ce message apparaît dans les fichiers `models.py` et `views.py`, et les numéros de lignes sont indiqués.

Django a détecté que le nouveau message, `Invalid mark`, ressemblait un peu a un qu'on avait déjà traduit, `Invalid data format`, et il a donc appliqué la même traduction. Évidemment ça marche pas trop, donc **il faut faire attention à remplacer la traduction**.

## Compiler les traductions

Une fois qu'on a tout traduit, il faut encore compiler ce fichier `django.po` en un fichier `django.mo`, plus efficace pendant l'exécution. On pourrait faire ça nous même après chaque nouvelle traduction, mais on risquerait d'oublier. On a donc plutôt mis la commande correspondante dans les fichiers bash entrypoint du backend :

```sh
python3 manage.py compilemessages --ignore "*/site-packages/*"
```

Comme ça, **les traductions sont compilées à chaque lancement de la Langate**. Cette compilation est très rapide, donc ça ne pose pas de problème.