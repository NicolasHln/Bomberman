#! /usr/bin/python3
# -*- coding: utf-8 -*-
#

# import des librairies standard de python
import sys
import random
import functools

# import librairies PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

# import des modules du jeu
from RenderArea import *
from Application import *
from Personnage import *
from Bombe import *
from Sound import *

# classe qui gère tout le jeu

class Controleur(QWidget):

    def __init__(self,nbPlayer):
        super().__init__()
        # Initialise le nombre de joueur, la map, persos,une listes qui contiendra les bombes, le renderArea et les sons
        self.nbPlayer=nbPlayer
        self.map=Map(nbPlayer)
        self.initCharacter(nbPlayer)
        self.bombs=[]
        self.renderArea=RenderArea(self.map,nbPlayer,self.character1,self.character2,self.character3,self.character4,self.bombs)
        self.sound=Sound()

    def initCharacter(self,nbPlayer):
        # Initialise les personnage par défaut
        self.character1=Perso("ninja",1,1,1)
        self.character2=Perso("cowboy",1,13,2)
        self.character3=Perso("chevalier",13,1,3)
        self.character4=Perso("indien",13,13,4)

    def movePlayer(self,id,deltaX,deltaY,dir):
        #met le sprite du perso allant vers dir
        character=self.getCharacterById(id)
        if not self.gameEnd() and character.vie>0:
            character.url="img/personnages/"+character.imgName+"/"+character.imgName+"_"+dir+"1.png"

            caseLibre=[1,7,8,9,10]
            # vérifie si le personnage peut se déplacer à x+deltaX,y+deltaY et change son x et y si c'est possible
            if ((character.x+deltaX<self.map.LARG-1) and (character.y+deltaY<self.map.LARG-1) and (character.x+deltaX>0) and (character.y+deltaY>0) and (self.map.grid[character.x+deltaX][character.y+deltaY] in caseLibre)):

                # vérifie si c'est un bonus
                if self.map.grid[character.x+deltaX][character.y+deltaY]==7:
                    character.feu+=1
                    self.sound.soundGetBonus.play()
                elif self.map.grid[character.x+deltaX][character.y+deltaY]==8:
                    character.vie+=1
                    self.sound.soundGetBonus.play()
                elif self.map.grid[character.x+deltaX][character.y+deltaY]==9:
                    character.score+=5
                    self.sound.soundGetBonus.play()
                    self.renderArea.updateScore()
                elif self.map.grid[character.x+deltaX][character.y+deltaY]==10:
                    character.maxBomb+=1
                    self.sound.soundGetBonus.play()
                # peu importe sa valeur on avance
                self.map.changeValue(character.x+deltaX,character.y+deltaY,2)

                if self.map.grid[character.x][character.y]==6:
                #si une bombe est posée, la case d'où l'on vient reste une bombe
                    self.map.changeValue(character.x,character.y,5)
                else:
                    self.map.changeValue(character.x,character.y,1)
                character.move(deltaX,deltaY)


    def putBomb(self,id):
        # crée un bombe et l'affiche aux coordonnées du personnage
        # recupère le personnage qui veut poser la bombe
        character=self.getCharacterById(id)
        # vérifie si la partie est en cours,que le perso n'est pas mort et qu'il n'as pas poser son max de bombes
        if not self.gameEnd() and character.vie>0 and self.nbBombPoser(id)<character.maxBomb:
            #si la bombe peut être posée, le son de pose de bombe est joué
            self.sound.soundPutBomb.play()
            bombe=Bombe(character)
            self.bombs.append(bombe)
            self.map.grid[bombe.x][bombe.y]=6
            self.bombTimer(bombe)

    def nbBombPoser(self,id):
        # renvoie le nombre de bombes posé par un personnage
        nbBomb=0
        for bomb in self.bombs:
            if bomb.character.id==id:
                nbBomb+=1
        return nbBomb

    def getCharacterAt(self,i,j):
        # renvoie le personnage a la position i,j ou 0 s'il n'y en pas
        if (self.character1.x,self.character1.y)==(i,j):
            return self.character1
        elif (self.character2.x,self.character2.y)==(i,j):
            return self.character2
        elif (self.character3.x,self.character3.y)==(i,j):
            return self.character3
        elif (self.character4.x,self.character4.y)==(i,j):
            return self.character4
        else:
            return 0

    def getCharacterById(self,id):
        # recupère le personnage par son id
        if self.character1.id==id:
            return self.character1
        elif self.character2.id==id:
            return self.character2
        elif self.character3.id==id:
            return self.character3
        elif self.character4.id==id:
            return self.character4


    def updateCharacterUrl(self):
        # met à jour les url des personnages (utilisés au choix des personnages)
        self.character1.updateUrl()
        self.character2.updateUrl()
        self.character3.updateUrl()
        self.character4.updateUrl()

    def bombTimer(self,bomb):
        #crée un Qtimer en singleShot et au bout de 3sec
        #recupére inRange et traite les données
        timer = QTimer(self)
        timer.setSingleShot(True)
        # functools.partial(func,param1,etc) permet de passer des paramètre a une fonction
        # ce que ne permet le timeout.connect à la base
        # cela a permis de factoriser le code
        timer.timeout.connect(functools.partial(self.explose, bomb))
        timer.start(3000)

    def explose(self,bomb):
        # fais exploser la bomb
        # recupère les obstacle dans sa portée
        obstacle=self.inRange(bomb)

        wallPos=[]
        # pour chaque postion d'obstacle
        for i,j in obstacle:
            # si c'est un joueur ou un ennemi
            if self.map.grid[i][j]==2 or self.map.grid[i][j]==4:
                # on recupère le personnage
                character=self.getCharacterAt(i,j)
                # on reduit sa vie
                character.reduitVie()
                # s'il est mort on augmente le score du poseur de bombe et met de la musique de mort
                if character.isDead():
                    self.sound.soundDeathEnemy.play()
                    bomb.character.score+=10
                self.map.changeValue(i,j,1)
            # si c'est une autre bombe
            elif self.map.grid[i][j]==5:
                # on appelle une fonction qui fait exploser la bombe
                self.exploseUneBombe(self.getBombAt((i,j)),[(bomb.x,bomb.y)])
            # si c'est une bombe et un personnage
            elif self.map.grid[i][j]==6:
                self.exploseUneBombe(self.getBombAt((i,j)),[(bomb.x,bomb.y)])
                character=self.getCharacterAt(i,j)
                character.reduitVie()
                if character.isDead():
                    self.sound.soundDeathPlayer.play()
                    self.map.changeValue(i,j,1)
            # si c'est un bloc destructible
            elif self.map.grid[i][j]==3:
                    # on appelle une fonction pour peut-être donner un bonus
                    wallPos.append((i,j))
                    # self.exploseBloc(i,j)
                    bomb.character.score+=1

        #à l'explosion de la bombe, le son d'explosion est joué
        self.sound.soundExplosionBomb.play()
        # vérifie si le jeu est fini
        self.gameEnd()
        # retire la bombe de
        self.map.changeValue(bomb.x,bomb.y,1)

        # tente de faire afficher l'explosion
        # fonctionne mais ne disparait pas
        self.putFlame(bomb,obstacle,wallPos)
        # enlève la bomb de la liste des bombes
        self.bombs.remove(bomb)
        # update
        self.renderArea.updateScore()
        self.renderArea.update()

    def exploseUneBombe(self,bomb,BombesParent):
        # sert à faire exploser une bombe en particulier qui serait inRange d'une autre
        # BombesParent est la liste des bombes précédentes pour ne pas faire une boucle dans la récursion
        # en voulant faire exploser le bombe parent

        obstacle=self.inRange(bomb)

        wallPos=[]
        # pour chaque postion d'obstacle
        for i,j in obstacle:
            # si c'est un joueur ou un ennemi
            if self.map.grid[i][j]==2 or self.map.grid[i][j]==4:
                # on recupère le personnage
                character=self.getCharacterAt(i,j)
                # on reduit sa vie
                character.reduitVie()
                # s'il est mort on augmente le score du poseur de bombe et met de la musique de mort
                if character.isDead():
                    self.sound.soundDeathEnemy.play()
                    bomb.character.score+=10
                self.map.changeValue(i,j,1)
            # si c'est une autre bombe
            elif self.map.grid[i][j]==5 and (i,j) not in BombesParent:
                # on appelle une fonction qui fait exploser la bombe
                BombesParent.append((bomb.x,bomb.y))
                self.exploseUneBombe(self.getBombAt((i,j)),BombesParent)
            # si c'est une bombe et un personnage
            elif self.map.grid[i][j]==6 and (i,j) not in BombesParent:
                BombesParent.append((bomb.x,bomb.y))
                self.exploseUneBombe(self.getBombAt((i,j)),BombesParent)
                character=self.getCharacterAt(i,j)
                character.reduitVie()
                if character.isDead():
                    self.sound.soundDeathPlayer.play()
                    self.map.changeValue(i,j,1)
            # si c'est un bloc destructible
            elif self.map.grid[i][j]==3:
                    # on appelle une fonction pour peut-être donner un bonus
                    wallPos.append((i,j))
                    # self.exploseBloc(i,j)
                    bomb.character.score+=1

        #à l'explosion de la bombe, le son d'explosion est joué
        self.sound.soundExplosionBomb.play()
        # vérifie si le jeu est fini
        self.gameEnd()
        # retire la bombe de
        self.map.changeValue(bomb.x,bomb.y,1)

        # tente de faire afficher l'explosion
        # fonctionne mais ne disparait pas
        self.putFlame(bomb,obstacle,wallPos)
        # enlève la bomb de la liste des bombes
        self.bombs.remove(bomb)
        # update
        self.renderArea.updateScore()
        self.renderArea.update()

    def exploseBloc(self,i,j):
        caseLibre=[7,8,9,10]
        # 20 pourcent de chance d'avoir un bonus choisi également au hassard
        if random.random()<0.20:
            self.map.changeValue(i,j,caseLibre[random.randint(0,len(caseLibre)-1)])
        else:
            self.map.changeValue(i,j,1)


    def putFlame(self,bomb,inRangeBomb,wallPos):
        # affiche les flammes

        # liste des postions où il y aura des flammes pour les enlever
        flamePos=[]

        # change la valeur pour le centre des flammes
        self.map.changeValue(bomb.x,bomb.y,11)
        flamePos.append((bomb.x,bomb.y))

        for i in range (1,2+bomb.character.feu):
            #Horizontalement vers la droite
            # si la case est dans la map et qu'il n'y rien qui la bloque avant ou une bombe
            if (bomb.x+i,bomb.y) in inRangeBomb or self.map.grid[bomb.x+i][bomb.y]==1:
                    self.map.changeValue(bomb.x+i,bomb.y,12)
                    flamePos.append((bomb.x+i,bomb.y))
            #Horizontalement vers la gauche
            # si la case est dans la map et qu'il n'y rien qui la bloque avant ou une bombe
            if (bomb.x-i,bomb.y) in inRangeBomb or self.map.grid[bomb.x-i][bomb.y]==1:
                        self.map.changeValue(bomb.x-i,bomb.y,12)
                        flamePos.append((bomb.x-i,bomb.y))
            #verticalement vers le bas
            # si la case est dans la map et qu'il n'y rien qui la bloque avant ou une bombe
            if (bomb.x,bomb.y+i) in inRangeBomb or self.map.grid[bomb.x][bomb.y+i]==1:
                        self.map.changeValue(bomb.x,bomb.y+i,13)
                        flamePos.append((bomb.x,bomb.y+i))

            #verticalement vers le haut
            # si la case est dans la map et qu'il n'y rien qui la bloque avant ou une bombe
            if (bomb.x,bomb.y-i) in inRangeBomb or self.map.grid[bomb.x][bomb.y-i]==1:
                        self.map.changeValue(bomb.x,bomb.y-i,13)
                        flamePos.append((bomb.x,bomb.y-i))
        self.update()
        self.renderArea.update()

        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(functools.partial(self.removeFlame,flamePos,wallPos))
        timer.start(500)

    def removeFlame(self,flamePos,wallPos):
        # retire les flammes

        # change la valeur en vérifiant s'il n'y pas un personnage
        for pos in flamePos:

            if self.getCharacterAt(pos[0],pos[1])!=0 :
                self.map.changeValue(pos[0],pos[1],2)
            elif pos in wallPos:
                self.exploseBloc(pos[0],pos[1])
            else:
                self.map.changeValue(pos[0],pos[1],1)
        self.update()
        self.renderArea.update()


    def getBombAt(self,pos):
        for bomb in self.bombs:
            if (bomb.x,bomb.y)==pos:
                return bomb

    def inRange(self,bomb):
        # renvoie une liste contenant les coordonées de ses obstacles
        obstacle=[]
        # print(bomb)
        list_destructible=[2,3,4,5]
        # vérifie si un joueur est encore à la position de la bombe
        if self.getCharacterAt(bomb.x,bomb.y)!=0:
            obstacle.append((bomb.x,bomb.y))

        # vérifie dans les 2 cases dans les 4 direction de la grille de la map si il y a d'autres bombes, des murs cassables ou personnages (player ou ennemies)

        # tant qu'il n'y a pas d'obstacle on regarde dans la portée de la bombe
        i=1
        libre=True
        while libre and i<2+bomb.character.feu:
            #Horizontalement vers la droite
            # si la case est dans la map et qu'il n'y rien qui la bloque avant ou une bombe
            if bomb.x+i>0 and bomb.x+i<self.map.LARG-1:
                if (self.map.grid[bomb.x+i-1][bomb.y]==1 or self.map.grid[bomb.x+i-1][bomb.y]==5) and self.map.grid[bomb.x+i][bomb.y] in list_destructible:
                    obstacle.append((bomb.x+i,bomb.y))
                else:
                    libre=False
            i+=1

            #Horizontalement vers la gauche
            # si la case est dans la map et qu'il n'y rien qui la bloque avant ou une bombe
        i=1
        libre=True
        while libre and i<2+bomb.character.feu:
            if bomb.x-i>0 and bomb.x-i<self.map.LARG-1:
                if (self.map.grid[bomb.x-i+1][bomb.y]==1 or self.map.grid[bomb.x-i+1][bomb.y]==5) and self.map.grid[bomb.x-i][bomb.y] in list_destructible:
                    obstacle.append((bomb.x-i,bomb.y))
                else:
                    libre=False
            i+=1
            #verticalement vers le bas
            # si la case est dans la map et qu'il n'y rien qui la bloque avant ou une bombe
        i=1
        libre=True
        while libre and i<2+bomb.character.feu:
            if bomb.y+i>0 and bomb.y+i<self.map.LARG-1:
                if(self.map.grid[bomb.x][bomb.y+i-1]==1 or self.map.grid[bomb.x][bomb.y+i-1]==5) and self.map.grid[bomb.x][bomb.y+i] in list_destructible:
                    obstacle.append((bomb.x,bomb.y+i))
                else:
                    libre=False
            i+=1
            #verticalement vers le haut
            # si la case est dans la map et qu'il n'y rien qui la bloque avant ou une bombe
        i=1
        libre=True
        while libre and i<2+bomb.character.feu:
            if bomb.y-i>0 and bomb.y-i<self.map.LARG-1:
                if(self.map.grid[bomb.x][bomb.y-i+1]==1 or self.map.grid[bomb.x][bomb.y-i+1]==5) and self.map.grid[bomb.x][bomb.y-i] in list_destructible:
                    obstacle.append((bomb.x,bomb.y-i))
                else:
                    libre=False
            i+=1

        return obstacle
        # DEFAUT :
        # ne s'arrête pas vraiment quand il y a un obstacle

    # vérifie si la partie est finie, renvoie True si c'est vrai
    def gameEnd(self):
            if self.gameWin():
                return True
            elif self.gameLose():
                return True
            else:
                return False

    def gameWin(self):
        # ne marche pas, ne finit jamais la partie
        if self.nbPlayer==1:
            # si il n'y qu'un joueur et que c'est le seul en vie il a gagné
            if self.character1.vie!=0 and self.character2.vie==0 and self.character3.vie==0 and self.character4==0:
                self.renderArea.displayEndGame(1,"gagné")
                return True
        else:
            # si 2 joueurs et que le premier est en vie il a gagné
            if self.character1.vie!=0 and self.character2.vie==0 and self.character3.vie==0 and self.character4==0:
                self.renderArea.displayEndGame(1,"gagné")
                return True
            # si 2 joueurs et que le deuxième est en vie il a gagné
            elif self.character1.vie==0 and self.character2.vie==0 and self.character3.vie==0 and self.character4!=0:
                self.renderArea.displayEndGame(2,"gagné")
                return True
            else:
                return False

    def gameLose(self):
        # ne marche qu'en 1 joueur
        if self.nbPlayer==1:
            if self.character1.vie==0:
                self.renderArea.displayEndGame(1,"perdu")
                return True
        else:
            if self.character1.vie==0 and self.character4==0:
                self.renderArea.displayEndGame(3,"perdu")
                return True
            else:
                return False
