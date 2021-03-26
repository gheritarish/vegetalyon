# Vegetalyon

## Cahier des charges
### Contexte
Lyon a lancé en 2017 le plan Canopé, un plan de végétalisation de la métropole lyonnaise, visant à planter un total de 300 000 arbres. Toutefois, il n'est pas si aisé de planter des arbres. En effet, chaque arbre a besoin de soleil pour pouvoir pousser, mais aussi d'eau, de place pour étendre ses racines, de temps et de place pour se développer, etc.
De plus, la végétalisation ne se limite pas uniquement aux arbres. Effectivement, il est possible de végétaliser une ville en utilisant des arbustes ou encore des potagers urbains.

Dans ce contexte, plusieurs points peuvent attirer notre attention. Tout d'abord, les zones qui sont déjà boisées ne sont pas celles à végétaliser en priorité, contrairement aux zones plus industrialisées.
De plus, la largeur des rues est un facteur à prendre en compte. En effet, des rues trop étroites ne paraissent pas, à première vue, être des endroits où planter des arbres imposants à cause du manque de place, alors que des arbustes en pot pourraient s'y épanouir.
Enfin, la question de la vue aérienne n'est pas à négliger. Si des toits bétonnés ne sont pas attirants pour l'œil, tous ne peuvent pas non plus être transformés en potagers ou parterres de fleurs si le soleil ne les atteint pas.

Ainsi, *VegetaLyon* s'inscrit dans le projet *DatAgora*, qui vise à analyser des données actuelles de manière croisée afin de déterminer comment placer des arbres en ville.

### Travail
Notre travail est documenté dans le Wiki de cette page Github, vous y trouverez le cahier des charges qui nous a été donné, les méthodes que nous avons utilisées pour implémenter notre code.

L'arborescence du Wiki est listée ci-dessous :


### Fichiers
* `README.md` : Ce fichier est celui que vous êtes en train de lire, il explique comment s'y retrouver dans le GitHub.
* `data` : Ce dossier contient les données utilisées pour le traitement des différents indicateurs.
* `produced_data` : Ce dossier contient les données qui découlent d'un traitement. Elles peuvent être soit des données finales prêtes à être visualisées, soit des données utiles pour d'autres traitements.
* `Grid.py` : Traitement permettant de réduire la grille de points utilisée pour les ombres. Il supprime les points qui sont dans les bâtiments, sur la chaussée et dans les parcs et jardins.
* `Shadows.py` : Attribution de score d'ombre à la grid, qui permet de déterminer les endroits de la zone qui sont le plus au soleil, compte tenu de l'ombre des bâtiments et des arbres sur place.
* `ToitsPlatsV2.ipynb` : 
* `Biophilie.ipynb` : 