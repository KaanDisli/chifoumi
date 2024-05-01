# -*- coding: utf-8 -*-

# Nicolas, 2024-02-09
from __future__ import absolute_import, print_function, unicode_literals

import random 
import numpy as np
import sys
from itertools import chain


import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme








# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'grid-chifoumi-map'
    game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    
    nbLignes = game.spriteBuilder.rowsize
    nbCols = game.spriteBuilder.colsize
    assert nbLignes == nbCols # a priori on souhaite un plateau carre
    lMin=2  # les limites du plateau de jeu (2 premieres lignes utilisees pour stocker les objets)
    lMax=nbLignes-2 
    cMin=2
    cMax=nbCols-2
   
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    
   
    
    # on definit les types d'items sur la carte
    items_types = {0:"flamme",1:"potion",2:"pumpkin"}

    def zone(k,pos,placed):
        (x,y) = pos
        if placed:
            if k==0: 
                return (x>2 and x<9 and y>2 and y<10) # zone des flammes
            elif k==1:
                return (x>12 and x<19 and y>2 and y<10) # zone des potions
            elif k==2:
                return (x>12 and x<19 and y>12 and y<19) # zone des citrouilles
        else: 
            if k==0: 
                return (x==0 or x==1) # zone des flammes
            elif k==1:
                return (y==0 or y==1) # zone des potions
            elif k==2:
                return (x==lMax or x==lMax+1) # zone des citrouilles
                
    
    nb_types = len(items_types)
    
    # on localise tous les objets a allouer au hasard
    # sur le layer ramassable
    # ceux deja places, et ceux a placer
    
    items_to_place = [[],[],[]]
    items_to_place[0] = [o for o in game.layers['ramassable'] if zone(0,o.get_rowcol(),False)]
    items_to_place[1] = [o for o in game.layers['ramassable'] if zone(1,o.get_rowcol(),False)]
    items_to_place[2] = [o for o in game.layers['ramassable'] if zone(2,o.get_rowcol(),False)]

    items_placed = [[],[],[]]
    items_placed[0] = [o for o in game.layers['ramassable'] if zone(0,o.get_rowcol(),True)]
    items_placed[1] = [o for o in game.layers['ramassable'] if zone(1,o.get_rowcol(),True)]   
    items_placed[2] = [o for o in game.layers['ramassable'] if zone(2,o.get_rowcol(),True)] 
    nbItems = len(items_to_place[0]+items_to_place[1]+items_to_place[2]),len(items_placed[0]+items_placed[1]+items_placed[2])
    picked_items = [[0,0,0],[0,0,0]] # compteur des items de chaque type pour chaque joueur
    
    #-------------------------------
    # Fonctions permettant de récupérer les listes des coordonnées
    # d'un ensemble d'objets ou de joueurs
    #-------------------------------
    
    def itemStates(items): 
        # donne la liste des coordonnees des items
        return [o.get_rowcol() for o in items]
    
    def playerStates(players):
        # donne la liste des coordonnees dez joueurs
        return [p.get_rowcol() for p in players]
    
   
    #-------------------------------
    # Rapport de ce qui est trouve sut la carte
    #-------------------------------
    print("lecture carte")
    print("-------------------------------------------")
    print('joueurs', nbPlayers)
    print("lignes", nbLignes)
    print("colonnes", nbCols)
    print("objets",nbItems)
    print("-------------------------------------------")

    #-------------------------------
    # Carte demo 
    # 2 joueurs 
    # Joueur 0: random walk
    # Joueur 1: A*
    #-------------------------------
    
        
    #-------------------------------

    #-------------------------------
    # Fonctions definissant les positions legales et placement de mur aléatoire
    #-------------------------------
    
    def legal_move_position(pos):
        row,col = pos
        # une position legale de deplacement est dans la carte 
        return (row>lMin and row<lMax-1 and col>=cMin and col<cMax)
    
    
    def legal_position(pos):
        row,col = pos
        all_items_placed = items_placed[0] + items_placed[1] + items_placed[2]
        # une position legale est dans la carte et pas sur un objet deja pose ni sur un joueur
        return ((pos not in itemStates(all_items_placed)) and (pos not in playerStates(players)) and row>lMin and row<lMax-1 and col>=cMin and col<cMax)
    
    def draw_random_location():
        # tire au hasard un couple de position permettant de placer un item
        while True:
            random_loc = (random.randint(lMin,lMax),random.randint(cMin,cMax))
            if legal_position(random_loc):
                return(random_loc)

    #-------------------------------
    # On place tous les items du bord au hasard
    #-------------------------------
                    
    for k in range(nb_types):                 
        for i in range(0,len(items_to_place[k])): 
            o = items_to_place[k][i]
            (x1,y1) = draw_random_location()
            o.set_rowcol(x1,y1)
            items_placed[k].append(o)
            game.mainiteration()
        
    print("Objets places:", len(items_placed[0]),len(items_placed[1]),len(items_placed[2]))

    #-------------------------------
    # On place tous les joueurs au hasard
    #-------------------------------
     
    for i in range(0,len(players)): 
        (x1,y1) = draw_random_location()
        players[i].set_rowcol(x1,y1)
        game.mainiteration()
    
    
    
    
    #-------------------------------
    # Fonctions du binôme
    #-------------------------------
        
    def move_randomly(row, col):
        """
        permet de deplacer un joueur aléatoirement
        """
        x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
        next_row = row+x_inc
        next_col = col+y_inc
        if legal_move_position((next_row,next_col)):
            return next_row, next_col
        return row, col
    
    def avoidItems(items) : 
        """
        permet d'eviter les bordures et tous les items passés en paramètre (on passe les coordonnees des items à éviter (i,j))
        """
        g =np.ones((nbLignes,nbCols),dtype=bool)
        if items :
            for w in items:      # on met False quand un item
                g[w]=False
        for i in range(nbLignes):                   # on exclut aussi les bordures du plateau
            g[0][i]=False
            g[1][i]=False
            g[nbLignes-1][i]=False
            g[nbLignes-2][i]=False
            g[i][0]=False
            g[i][1]=False
            g[i][nbLignes-1]=False
            g[i][nbLignes-2]=False
        return g
    
    def rayon_visibilite(row_player, col_player,rayon, items_placed, desired) : 
        """
        permet de retourner les coordonnées d'un objet desirée dans le rayon de visibilité et une liste des items à éviter
        """
        item_desired = None
        items_to_avoid = []

        for i in range(row_player -rayon, row_player+rayon+1):
            for j in range(col_player -rayon, col_player+rayon+1):
                if (i,j) in itemStates(items_placed[desired]):
                    item_desired = (i,j)   # on a trouvé un objet désiré 
                elif (i,j) in itemStates(items_placed[not desired]):
                    items_to_avoid.append((i,j)) # on stock les objer a éviter (differenrs de l'objet désiré)

        return item_desired, items_to_avoid
  
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
            
    posPlayers = playerStates(players)
    row,col = posPlayers[0]
    row_1,col_1 = posPlayers[1]
    rayon = 3   # rayon de visibilite du joueur 1
    desired = 0 # objet désiré par le joueur 1
    target = None # position de l'objet désiré
    to_avoid = [] # liste des objets à éviter
    path = [] # chemin trouvé pour rejoindre l'objet désiré
    g = [] # liste des obstacles à éviter


    for i in range(iterations):
        
        #-------------------------------
        # on fait bouger le joueur 0 au hasard
        #-------------------------------

        
        while True: # tant que pas legal on retire une position
            x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
            next_row = row+x_inc
            next_col = col+y_inc
            if legal_move_position((next_row,next_col)):
                break
        players[0].set_rowcol(next_row,next_col)
        print ("pos 0:", next_row,next_col)
    
        col=next_col
        row=next_row
        posPlayers[0]=(row,col)
        
        for k in range(nb_types):
            if posPlayers[0] in itemStates(items_placed[k]):
                print("Trouvé ",items_types[k])
                picked_items[0][k]+=1
                o=players[0].ramasse(game.layers) # on recupere l'objet 
                items_placed[k].remove(o)         # on l'enleve de la liste des objets de ce type
                break


        #-------------------------------
        # on fait bouger le joueur 1 au hasard
        #-------------------------------
            

        g =np.ones((nbLignes,nbCols),dtype=bool)
        while True: 
            print("CHECK 0")
            print("target",target) 
            print("to avoid",to_avoid)    
            print("path",path)

            # SI UN OBJET DESIRE EST DETECTÉ    
            # on veut que le joueur 1 rejoigne l'obstacle désiré si il est dans son rayon de visibilité
            if target:
                print("CHECK 1")
                
                # 1) on deplace le joueur 1 jusqu'à l'objet désiré en suivant le chemin trouvé avec A* en faisant une seule étape
                # on fait l'etape en tete de liste et on la supprime
                if path:
                    # on fait le premier pas du chemin toruvé
                    row_1,col_1 = path[0]
                    players[1].set_rowcol(row_1,col_1)
                    posPlayers[1]=(row_1,col_1)
                    print ("pos joueur 1:", row_1,col_1)
                    path.pop(0) # on enleve l'etape courante

                    # 2.a) si on a trouvé le joueur 0 on joue au chifoumi	
                    if (row_1,col_1) == posPlayers[0]:
                        print("Let's play Chifoumi!")
                        break
                        
                    # 2.b) si on trouve un objet désiré on le ramasse et on met à jour nos variables
                    if posPlayers[1] in itemStates(items_placed[desired]):
                        print("Trouvé ",items_types[desired])
                        picked_items[1][desired]+=1
                        o=players[1].ramasse(game.layers) # on recupere l'objet
                        items_placed[desired].remove(o)
                        # on remet à jour les variables
                        to_avoid = []
                        path = []
                        target = None
                        break

                # if not target make it move randomly and look for the desired item  
            else:
                print("CHECK 2")
                next_row, next_col = move_randomly(row_1, col_1)

                # deplacement aléatoire du joueur 1
                players[1].set_rowcol(next_row,next_col)
                col_1=next_col
                row_1=next_row
                posPlayers[1]=(row_1,col_1)
                print ("pos 1:", next_row,next_col)

                # on regarde le rayon de visibilité du joueur 1
                target, to_avoid = rayon_visibilite(row_1, col_1, rayon, items_placed, desired)
                g = avoidItems(to_avoid)

                # on trouve le chemin pour rejoindre l'objet désiré
                if target:
                    p = ProblemeGrid2D(posPlayers[1],target,g,'manhattan')
                    path = probleme.astar(p,verbose=False)
                    print ("Chemin trouvé:", path)

            break

        
        # mise à jour du pleateau de jeu
        game.mainiteration()

    
            
    
    pygame.quit()
    
    
    
    
    #-------------------------------
    
        
    
    
   

if __name__ == '__main__':
    main()
    


