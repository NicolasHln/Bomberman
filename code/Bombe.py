#! /usr/bin/python3
# -*- coding: utf-8 -*-
#

from Personnage import *
from Application import *
from Window import *
from Map import *

# classe de la bombe

class Bombe(QWidget):

    def __init__(self,character):
        super().__init__()
        # on sauvegarde le personnage pour les coordonées de la bombe au postion du personnage
        # ainsi que son score et sa puissance de feu
        # ainsi qrecupère ses info telle que sa puissance de feu
        self.character=character
        self.x=character.x
        self.y=character.y
        self.feu=character.feu
