#! /usr/bin/python3
# -*- coding: utf-8 -*-
#

# import des librairies standard de python
import sys
from math import *

# import librairies PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# import des modules du jeu
from Personnage import *
from Application import *
from Window import *
from Map import *
from Bombe import *


#classe qui gère l'affichage du jeu
class RenderArea(QWidget):
    def __init__(self,map,nbPlayer,character1,character2,character3,character4,bombs, parent=None):
        super(RenderArea,self).__init__(parent)
        self.initUI()

        # recupère la map
        self.map=map

        # recupère les 4 personnages
        self.character1=character1
        self.character2=character2
        self.character3=character3
        self.character4=character4
        self.nbPlayer=nbPlayer

        self.initBlockSize()
        #affiche le score
        self.displayScore()

    def initBlockSize(self):
        #calcule la taille des blocs en fonction de la taille de la fenêtre
        #15 blocs sur 90% de la hauteur

        # ne fonctionne pas car sur des écrans 720p le bas de la map est coupé
        self.blockSize=(QDesktopWidget().availableGeometry().height()*0.75)//self.map.LONG

    def initUI(self):
        self.pen = QPen(QColor(125,155,155))
        self.pen.setWidth(3)
        self.brush = Qt.NoBrush

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.setBrush(self.brush)

        # dessine la map
        self.drawMap(self.painter)
        # finit le painter pour lui permettre de s'actualiser à chaque événement
        self.painter.end()


    def displayScore(self):
        #l'initialisation du jeu crée le score pour le mode 1 joueur
        # Initialise et place quand même le score du joueur2 au cas où on joue en 2 joueurs
            self.score1=QLabel(self)
            self.score2=QLabel(self)
            self.score1.setText("Score joueur: "+ str(self.character1.score)+" ")
            self.score1.setStyleSheet("background: #00FFFFFF; border-radius: 10px; color: black; font: bold 30px; border: 1.5px solid blue; height: 85; width: 305; margin: 8px;")
            self.score1.move(self.frameGeometry().width()-600,self.frameGeometry().height())
            self.score2.move(self.frameGeometry().width()-600,self.frameGeometry().height()+100)

    def updateScore(self):
        #le deuxième score s'affiche en mode deux joueurs, et chaque score se met à jour en fonction du character.score
        if self.nbPlayer==1:
            self.score1.setText("Score joueur: "+ str(self.character1.score)+" ")
            self.score1.show()
        else:
            self.score1.setText("Score joueur 1: "+ str(self.character1.score)+" ")
            self.score1.show()
            self.score2.setText("Score joueur 2: "+ str(self.character4.score)+" ")
            self.score2.setStyleSheet("background: #00FFFFFF; border-radius: 10px; color: black; font: bold 30px; border: 1.5px solid blue; height: 85; width: 305; margin: 8px;}")
            self.score2.show()

    def drawMap(self,painter):
        #calcule le point d'origne du terrain c'est a dire le point le plus en haut à gauche du terrain pour que le terrain soit au milieu de l'écran
        self.originX = (self.frameGeometry().width()/2)-(self.blockSize*self.map.LARG/2)
        self.originY = (self.frameGeometry().height()/2)-(self.blockSize*self.map.LONG/2)

        #dessine le terrain en fonction de la valeur contenue dans grid de self.map
        for i in range(self.map.LONG):
            for j in range(self.map.LARG):

                r=QRect(QPoint(self.originX+(self.blockSize*i),self.originY+(self.blockSize*j)),QSize(self.blockSize,self.blockSize))

                if(self.map.grid[i][j]==0):
                    #dessine un mur incassable

                    # si le mur est une des colonne aux extremités les sprites sont différents car ils sont collés
                    if(i==0 or i==self.map.LARG-1) and (j!=self.map.LONG-1):
                        # rectangle de la colonne gauche
                        r2=QRect(QPoint(self.originX+(self.blockSize*0),self.originY+(self.blockSize*j)),QSize(self.blockSize,self.blockSize))
                        painter.drawPixmap(r2,QPixmap("img/Blocs/blocMetal2.png").scaled(self.blockSize,self.blockSize))

                        # rectangle de la colonne droite
                        r3=QRect(QPoint(self.originX+(self.blockSize*(self.map.LONG-1)),self.originY+(self.blockSize*j)),QSize(self.blockSize,self.blockSize))

                        painter.drawPixmap(r3,QPixmap("img/Blocs/blocMetal2.png").scaled(self.blockSize,self.blockSize))
                    else:
                        #sinon c'est un bloc normal
                        painter.drawPixmap(r,QPixmap("img/Blocs/blocMetal.png").scaled(self.blockSize,self.blockSize))

                elif(self.map.grid[i][j]==1):
                    #dessine le sol
                    painter.drawPixmap(r,QPixmap("img/Blocs/sol.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))

                elif(self.map.grid[i][j]==2):
                    #dessine la case du personnage
                    self.drawCharacter(painter,i,j)

                elif(self.map.grid[i][j]==3):
                    #dessine les murs cassables
                    painter.drawPixmap(r,QPixmap("img/Blocs/wall.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))

                elif(self.map.grid[i][j]==4):
                    #dessine la case de l'ennemi
                    self.drawCharacter(painter,i,j)

                elif (self.map.grid[i][j]==5):
                    #dessine la bombe
                    painter.drawPixmap(r,QPixmap("img/Blocs/sol.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))
                    self.drawBomb(painter,i,j)

                elif self.map.grid[i][j]==6:
                    self.drawCharacter(painter,i,j)
                    self.drawBomb(painter,i,j)

                elif (self.map.grid[i][j]==7):
                    #dessine le bonus de feu
                    painter.drawPixmap(r,QPixmap("img/Blocs/sol.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))
                    painter.drawPixmap(r,QPixmap("img/Bonus/fireBonus.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))

                elif (self.map.grid[i][j]==8):
                    #dessine le bonus de vie
                    painter.drawPixmap(r,QPixmap("img/Blocs/sol.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))
                    painter.drawPixmap(r,QPixmap("img/Bonus/lifeBonus.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))
                elif (self.map.grid[i][j]==9):
                    #dessine le bonus de score
                    painter.drawPixmap(r,QPixmap("img/Blocs/sol.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))
                    painter.drawPixmap(r,QPixmap("img/Bonus/scoreBonus.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))

                elif (self.map.grid[i][j]==10):
                    #dessine le bonus de bombe
                    painter.drawPixmap(r,QPixmap("img/Blocs/sol.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))
                    painter.drawPixmap(r,QPixmap("img/Bonus/bombBonus.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))

                elif self.map.grid[i][j]==11:
                    #dessine les flammes au centre de l'explosion
                    painter.drawPixmap(r,QPixmap("img/Blocs/sol.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))
                    painter.drawPixmap(r,QPixmap("img/bombe/ExplosionCentre.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))
                elif self.map.grid[i][j]==12:
                    #dessine les flammes à l'Horizontal
                    painter.drawPixmap(r,QPixmap("img/Blocs/sol.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))
                    painter.drawPixmap(r,QPixmap("img/bombe/ExplosionMid2.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))
                elif self.map.grid[i][j]==13:
                    #dessine les flammes à la verticale
                    painter.drawPixmap(r,QPixmap("img/Blocs/sol.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))
                    painter.drawPixmap(r,QPixmap("img/bombe/ExplosionMid1.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))



    def drawCharacter(self,painter,i,j):
        # dessine le sol puis le personnage en fonction de sa position
        character=self.getCharacterAt(i,j)

        r=QRect(QPoint(self.originX+(self.blockSize*i),self.originY+(self.blockSize*j)),QSize(self.blockSize,self.blockSize))
        painter.drawPixmap(r,QPixmap("img/Blocs/sol.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))
        painter.drawPixmap(r,QPixmap(character.url).scaled(self.blockSize,self.blockSize))

    def drawBomb(self,painter,i,j):
        #dessine  la bombe
        r=QRect(QPoint(self.originX+(self.blockSize*i),self.originY+(self.blockSize*j)),QSize(self.blockSize,self.blockSize))
        painter.drawPixmap(r,QPixmap("img/bombe/bombe1.png").scaled(self.blockSize,self.blockSize,Qt.KeepAspectRatioByExpanding,))

    def getCharacterAt(self,i,j):
        # renvoie le personnage à la position (i,j)
        if (self.character1.x,self.character1.y)==(i,j):
            return self.character1
        elif (self.character2.x,self.character2.y)==(i,j):
            return self.character2
        elif (self.character3.x,self.character3.y)==(i,j):
            return self.character3
        elif (self.character4.x,self.character4.y)==(i,j):
            return self.character4

    def displayEndGame(self,id,state):
        # affiche une phrase disant qui a gagne ou perdu et si c'est perdu affiche une image de fin de partie
        self.endImg=QLabel(self)
        if state=="perdu":
            self.endImg.setPixmap(QPixmap("img/Imagefond/game_over.png"))
            self.endImg.move(self.frameGeometry().width()/2,self.frameGeometry().height()/2)
            self.endImg.show()
        self.end=QLabel(self)
        if id!=3:
            self.end.setText("joueur : "+str(id)+" a "+state+" ")
        else:
            self.end.setText("les joueurs : "+" ont "+state+" ")
        self.end.move(self.frameGeometry().width()/2,self.frameGeometry().height()/2)
        self.end.show()
