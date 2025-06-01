### Script python pour comparer les baromètres de la FUB 2019 et 2021

Données à télécharger et à placer dans le dossier data/
- Contours des communes issues de OpenStreetMap (https://www.data.gouv.fr/fr/datasets/decoupage-administratif-communal-francais-issu-d-openstreetmap/): https://www.data.gouv.fr/fr/datasets/decoupage-administratif-communal-francais-issu-d-openstreetmap/#/resources/17062524-991f-4e13-9bf0-b410cc2216fd


Installation des dépendances
`uv sync`

Scripts:
- barometre_dep.py: calcule les evolutions et génère les cartes sauvegardées dans le dossier png, créé un tweet par département

Sorties:
- dossier png/: une image par département + une image de la France Métropolitaine
- dossier output/:
  * commune_qualif.csv: fichier recapitulatif des evolutions absolues et relative par département
  * tweets: fichier recapitulatif des tweets par département
