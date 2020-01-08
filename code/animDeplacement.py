#! /usr/bin/python3
# -*- coding: utf-8 -*-
#from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
import random
import sys
import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Bombe import *

# Fichier qui a servi a tester de faire l'animation du personnage qui se déplace que l'on a pas reussi à implémenter en jeu
# pour faire charger les images le fichier est à lancer dans le /code

class Example(QWidget):

    size=100
    imgNum=0
    imgQuantity=2

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color:transparent;")
        self.setGeometry(100, 100, 100, 100)
        self.label=QLabel(self)
        self.pixmaps=[QPixmap('../img/personnages/ninja/ninja_up1.png'),QPixmap('../img/personnages/ninja/ninja_up2.png'),QPixmap('../img/personnages/ninja/ninja.png')]
        for x in range(len(self.pixmaps)):
            self.pixmaps[x]=self.pixmaps[x].scaled(self.size,self.size,Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmaps[2])
        self.resize(self.pixmaps[2].width(),self.pixmaps[2].height())
        self.changeTimer=QTimer(self)
        self.changeTimer.timeout.connect(self.onTimeout)
        self.show()

    def moving(self):
        self.distance=20
        self.changeTimer.start(50)

    def onTimeout(self):
        #tant que l'image doit bouger (distance>0) alors l'image change (alterne pied droit et pied gauche)
        direct=self.direct

        if self.distance == 0:
            self.changeTimer.stop()
            self.label.setPixmap(self.pixmaps[2])

        else:
            self.changeFoot()
            self.move(self.x()+5*direct[0],self.y()+5*direct[1])
        self.distance -= 1

    def changeFoot(self): #alterne les images pour faire marcher le personnage
        if self.imgNum<self.imgQuantity-1:
            self.imgNum+=1
        else :
            self.imgNum=0
        self.label.setPixmap(self.pixmaps[self.imgNum])

    def setBomb(self):
        self.bombe=Bomb()



    def keyPressEvent(self, event):#gère la direction de l'animation en fonction de la touche, on fournit une liste d'images différente en fonction du personnage choisi
        direct=[0,0]
        key=event.key()

        if key == Qt.Key_Escape:
            # sys.exit()
            QCoreApplication.instance().quit()
        elif key==Qt.Key_Left:
            self.pixmaps=[QPixmap('../img/personnages/ninja/ninja_left1.png'),QPixmap('../img/personnages/ninja/ninja_left2.png'),QPixmap('../img/personnages/ninja/ninja_left3.png'),QPixmap('../img/personnages/chevalier/chevalier.png')]
            if event.isAutoRepeat():
                self.distance=1
                return
            self.direct=[-1,0]
            self.moving()
        elif key==Qt.Key_Right:
            self.pixmaps=[QPixmap('../img/personnages/ninja/ninja_right3.png'),QPixmap('../img/personnages/ninja/ninja_right2.png'),QPixmap('../img/personnages/ninja/ninja_right1.png')]
            if event.isAutoRepeat():
                self.distance=1
                return
            self.direct=[1,0]
            self.moving()
        elif key==Qt.Key_Up:
            self.pixmaps=[QPixmap('../img/personnages/ninja/ninja_up3.png'),QPixmap('../img/personnages/ninja/ninja_up2.png'),QPixmap('../img/personnages/ninja/ninja_up1.png')]
            if event.isAutoRepeat():
                self.distance=1
                return
            self.direct=[0,-1]
            self.moving()
        elif key==Qt.Key_Down:
            self.pixmaps=[QPixmap('../img/personnages/ninja/ninja_down3.png'),QPixmap('../img/personnages/ninja/ninja_down2.png'),QPixmap('../img/personnages/cowboy/cowboy.png')]
            if event.isAutoRepeat():
                self.distance=1
                return
            self.direct=[0,1]
            self.moving()
        elif key==Qt.Key_Space:
            self.setBomb()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
