[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/KDJwxQ6K)
# grid-chifoumi
template pour le projet 2024 IA et Jeux

## Présentation générale du projet

On propose dans ce projet d'implémenter une version spatialisée du jeu Chifoumi (Pierre, Feuille, Ciseaux). 
On s'inspire librement des verions spatialisées de ce jeu récemment proposées (voir Bibliographie). 
Le principe général du jeu est le suivant: trois types d'objets sont présents sur un terrain (une grille de jeu): des flammes, des potions, ou des citrouilles. La potion bat la flamme, la flamme bat la citrouille, et la citrouille bat la potion (ne me demandez pas pourquoi). 

Dans la configuration initiale, 6 potions, 6 flammes, et 6 citrouilles sont disposées à des positions prédéfinies. Un certain nombre d'autres objets de ces types sont ensuite disposés aléatoirement sur la grille. Les joueurs sont eux-mêmes disposés aléatoirement. Ils vont pouvoir ramasser ces objets et les placer dans leur sac. 

Les joueurs ont une **observabilité partielle de l'environnement**, ce qui signifie qu'ils perçoivent seulement une région autour d'eux (que l'on pourra paramétrer, par exemple en considérant les cases autour du joueur). **Aucune connaissance n'est supposée**: en particulier, les joueurs ne connaissent pas l'état du sac de l'autre joueur, et ils ne connaissent pas les emplacements des différents objets sur la carte. 

Les joueurs jouent **à tour de rôle**, en effectuant un coup à chaque fois. 
Les coups possibles sont:
* le **déplacement** de son joueur. Il est possible de se déplacer d'une case, dans toutes les directions sauf les diagonales. On suppose ici que les joueurs ne se bloquent pas entre eux, et qu'ils peuvent éventuellement être sur la même case à un moment donné. 
* le **déclenchement du chifoumi**. Il faut pour que l'autre joueur se situe dans sa région de visibilité. Toutefois il n'est pas obligatoire de déclencher le chifoumi. 
* lorsqu'un joueur se trouve sur une case comportant un objet d'un certain type, **il le ramasse nécessairement**. 


Lorsqu'un **duel de chifoumi** est déclenché, les règles sont les suivantes:
* chaque joueur joue nécessairement selon une stratégie mixte qui est donnée par la répartition des objets ramassés. Ainsi, un joueur qui aurait ramassé 2 flammes, 1 potion, et 1 citrouille va jouer avec 50% de chance la flamme, avec 25% la potion, et avec 25% la citrouille. Un joueur qui n'a rien ramassé joue selon la stratégie uniforme. Un joueur qui n'a ramassé qu'une citrouille va nécessairement jouer citrouille. 
* Les joueurs reçoivent les gains résultant de la bataille. Les objets sont replacés et une nouvelle partie commence. Les points gagnés sont donnés par la matrice classique : 1 point pour une victoire, 0 pour un match nul, -1 pour une défaite. 
* les parties sont limitées en nombre de tours. Si aucun chifoumi n'a eu lieu à cette limite, la partie est nulle. 
* après le duel de chifoumi ou avoir atteint le nombre de tour max la partie est terminée
* à la fin d'une partie, le joueur perdant réinitialise son sac (et donc sa stratégie). Si il s'agit d'un match nul les deux inventaires sont conservés.  
* puis une nouvelle partie commence en réallouant les joueurs et les objets sur la carte


Un **match** se déroule en un nombre pré-déterminé de parties (par exemple, 10), en cumulant les points. 
En cas d'égalité, c'est le joueur qui a déclenché le plus de batailles de chifoumi qui remporte la manche. 
Les joueurs peuvent se remémorer tout ce qu'ils veulent au cours d'une partie, et même d'un match en entier. Par exemple, le joueur peut se souvenir des coups joués par l'autre joueur lors des précédentes parties. 
 

**Version Arène** 
Note: bien que présenté ici pour 2 joueurs, le jeu peut être joué en version arène à 5 joueurs. Dans ce cas, les parties ont un plus grand nombre pré-déterminé de tours (par ex. 1000). Le joueur perdant lors d'un chifoumi vide son sac, réinitialise sa stratégie, et ne joue pas pendant 50 tours. Nous laissons cette perspective comme extension possible de votre projet.

### Bibilographie
Articles de recherche ayant servi d'inspiration 
* [Scalable Evaluation of Multi-Agent Learning with Melting Pot](https://arxiv.org/pdf/2107.06857.pdf)
* [Options as responses](https://arxiv.org/pdf/1906.01470.pdf)

## Modules disponibles

### Module pySpriteWorld

Pour la partie graphique, vous utiliserez le module `pySpriteWorld` (développé par Yann Chevaleyre) qui s'appuie sur `pygame` et permet de manipuler simplement des personnages (sprites), cartes, et autres objets à l'écran.

Une carte par défaut vous est proposée pour ce projet (`quoridorMap`): elle comporte 2 joueurs.
Les murs de chaque joueur sont initialement placés derrière lui. Dans cette carte, chaque joueur dispose de 15 murs, mais cela peut facilement être modifié.

La gestion de la carte s'opère grâce à des calques:
* un calque `joueur`, où seront présents les joueurs
* un calque `ramassable`, qui contient ici les murs


Les joueurs et les ramassables sont des objets Python sur lesquels vous pouvez effectuer des opérations classiques.
Par exemple, il est possible récupérer leurs coordonnées sur la carte avec `o.get_rowcol(x,y)` ou à l'inverse fixer leurs coordonnées avec `o.set_rowcol(x,y)`.
La mise à jour sur l'affichage est effective lorsque `mainiteration()` est appelé.


Notez que vous pourrez ensuite éditer vos propres cartes à l'aide de l'éditeur [Tiled](https://www.mapeditor.org/), et exporter ces cartes au format `.json`. Vous pourrez alors modifier le nombre de joueurs ou de murs disponibles, par exemple.

Il est ensuite possible de changer la carte utilisée en modifiant le nom de la carte utilisée dans la fonction `init` du `main`:
`name = _boardname if _boardname is not None else 'quoridorMap'``

:warning: Vous n'avez pas à modifier le code de `pySpriteWorld`

### Module search

Le module `search` qui accompagne le cours est également disponible. Il permet en particulier de créer des problèmes de type grille et donc d'appeler directement certains algorithmes de recherche à base d'heuristiques vus en cours, comme A:star: pour la recherche de chemin.

## Travail demandé

### Semaine 1
**Prise en main**. A l'éxécution du fichier `main.py`, vous devez observer le comportement suivant: un joueur se déplace de manière aléatoire (l'autre ne bouge pas pendant ce temps). Après 100 itérations, le deuxième joueur se déplace vers le premier en utilisant l'algorithme A* et en évitant tous les objets encore présents sur la carte. 

Evidemment tout ceci ne respecte pas du tout les règles du jeu.

:point_right: votre objectif lors de cette première séance est de faire jouer l'un contre l'autre un joueur complètement aléatoire (**stratégie random**) et un joueur qui se déplace aléatoirement mais qui va chercher un certain type d'objet, toujours le même, par ex. les flammes, dès qu'un objet de ce type apparait dans sa région de visibilité (on rappelle que la région d'observabilité est limitée), et sans ramasser d'autres objets au passage (**stratégie focused**). Dès qu'un joueur entre dans la région de l'autre joueur, ce dernier déclenche un chifoumi.  
 

### Semaine 2 et 3
**Mise en place et test de différentes stratégies**. Vous vous inspirerez des méthodes vues en cours pour proposer au moins 3 stratégies en plus des stratégies aléatoires élaborées en première semaine.
Vous comparerez chacune de ces stratégies en les faisant jouer les unes contre les autres.


### Semaine 4
**Soutenances**. Celles-ci ont lieu en binôme. Vous présenterez les principaux résultats de votre projet.
Le rapport doit être rédigé en markdown dans le fichier prévu à cet effet dans le répertoire `docs` (voir le template `rapport.md`).

