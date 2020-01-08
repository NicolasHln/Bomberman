#! /usr/bin/python3
# -*- coding: utf-8 -*-
#from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
import random
import sys
import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
import os


class Sound(QWidget):
    def __init__(self):
        super().__init__()

        # playlists des différents sons d'une partie, une pour chaque son
        self.playlist1 = QMediaPlaylist()
        self.playlist2 = QMediaPlaylist()
        self.playlist3 = QMediaPlaylist()
        self.playlist4 = QMediaPlaylist()
        self.playlist5 = QMediaPlaylist()

        #charque QUrl est relié à un son différent dans le dossier Sound
        putBomb = QUrl.fromLocalFile(os.getcwd() +"/sound/BombSound/poserBomb.wav")
        explosion = QUrl.fromLocalFile(os.getcwd() +"/sound/BombSound/explosion.wav")
        deathPlayer = QUrl.fromLocalFile(os.getcwd() +"/sound/PlayerSound/playerDeath.wav")
        deathEnemy = QUrl.fromLocalFile(os.getcwd() +"/sound/EnemySound/EnemyDeath.wav")
        getBonus = QUrl.fromLocalFile(os.getcwd() +"/sound/BonusSound/getBonus.wav")

        #puis on rajoute chaque son créé dans la playlist choisie
        self.playlist1.addMedia(QMediaContent(putBomb))
        self.playlist2.addMedia(QMediaContent(explosion))
        self.playlist3.addMedia(QMediaContent(deathPlayer))
        self.playlist4.addMedia(QMediaContent(deathEnemy))
        self.playlist5.addMedia(QMediaContent(getBonus))

        #le son ne sera joué qu'une fois, pas en boucle
        self.playlist1.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)
        self.playlist2.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)
        self.playlist3.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)
        self.playlist4.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)
        self.playlist5.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)

        #puis on crée un QMediaPlayer pour chaque son, auquel on ajoute la playlist contenant le son correspondant
        self.soundPutBomb = QMediaPlayer()
        self.soundPutBomb.setPlaylist(self.playlist1)
        self.soundExplosionBomb = QMediaPlayer()
        self.soundExplosionBomb.setPlaylist(self.playlist2)
        self.soundDeathPlayer = QMediaPlayer()
        self.soundDeathPlayer.setPlaylist(self.playlist3)
        self.soundDeathEnemy = QMediaPlayer()
        self.soundDeathEnemy.setPlaylist(self.playlist4)
        self.soundGetBonus = QMediaPlayer()
        self.soundGetBonus.setPlaylist(self.playlist5)
