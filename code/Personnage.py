#!/usr/bin/python3

import sys
from math import *

#classe du Personnage permettant de gérer sa vie, actions etc

class Perso:

    def __init__(self,imgName,x,y,id):
        # initialise ses attributs
        self.vie=1
        self.id=id
        self.x=x
        self.y=y
        self.score = 0
        # imgName represente le perso choisi
        self.imgName=imgName
        # url de l'image en fonction du perso
        self.url="img/personnages/"+self.imgName+"/"+self.imgName+".png"
        self.feu=0 #puissance de feu qui augmente avec les bonus
        self.maxBomb=1 #nombre de bombe posable à la fois

    # déplace le personnage
    def move(self,deltaX,deltaY):
        self.x+=deltaX
        self.y+=deltaY

    # met à jour l'url (utilisé quand on se déplace)
    def updateUrl(self):
        self.url="img/personnages/"+self.imgName+"/"+self.imgName+".png"

    # reduite la vie de 1 lorsque l'on a été touché par une bombe
    # si l'on a plus de vie nos coordonées sont en dehors de la map
    def reduitVie(self):
        if self.vie-1<=0:
            self.x=-1
            self.y=-1
        self.vie-=1

    # vérifie si le personnage est mort
    def isDead(self):
        if(self.vie==0):
            return self.vie<=0
