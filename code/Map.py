#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# import sys
from math import *

from Personnage import *
from Application import *
from Window import *
from RenderArea import *
from random import random

class Map():
    #classe contenant la matrice de la carte, matrice rempli d'entiers
    #0 pour un mur incassable,
    #1 pour vide,
    #2 pour des perso,
    #3 pour des murs cassables
    #4 pour des ennemies
    #5 bombe
    #6 pour une bombe et le perso
    #7 pour un bonus de puissance de feu
    #8 pour un bonus de vie
    #9 pour un bonus points
    #10 pour un bonus de  bombe en +
    #11 pour l'explosion
    def __init__(self,nbPlayer):
        #taille de la matrice
        self.LONG=15
        self.LARG=15
        self.grid=self.initGrid(nbPlayer)

    def initGrid(self,nbPlayer):
        #initialise et retourne la matrice du terrain
        grid=[]

        #liste des cases de départ à garder vide
        case_dep=[(2,1),(1,2),(1,12),(2,13),(12,1),(13,2),(12,13),(13,12)]

        # si il n'y qu'un joueur on met un personnage et 3 ennemies
        if nbPlayer==1:
            case_perso=[(1,1)]
            case_enemy=[(1,13),(13,1),(13,13)]

        # s'il y a 2 joueurs on met 2 personnage et 2 ennemies
        elif nbPlayer==2:
            case_perso=[(1,1),(13,13)]
            case_enemy=[(1,13),(13,1)]

        for i in range(self.LONG):
            line=[]
            if (i==0) or (i==self.LONG-1):
                #premiere ou dernière ligne
                for j in range(self.LARG):
                    line.append(0)
            else:
                for j in range(self.LARG):
                    if (j==0) or (j==14):
                        #colonne de début ou fin
                        line.append(0)
                    elif (i%2==0) and (j%2==0):
                        #blocs incassable dans la terrain
                        line.append(0)
                    elif (i,j) in case_dep:
                        #case de départ à garder vide
                        line.append(1)
                    elif (i,j) in case_perso:
                        #case de départ du perso
                        line.append(2)
                    elif (i,j) in case_enemy:
                        # case des ennemies
                        line.append(4)
                    else:
                        #ajout des blocs destructible de manière aleatoire
                        if(random()<0.70):
                            line.append(3)
                        else:
                            line.append(1)
            grid.append(line)
        return grid

    # change la valeur à la position i,j
    def changeValue(self,i,j,value):
        self.grid[i][j]=value
