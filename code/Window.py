#! /usr/bin/python3
# -*- coding: utf-8 -*-

# import des librairies standard de python
import sys
import os
import functools #sert pour les clicked.connect
from math import *

# import librairies PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

# import des modules du jeu
from RenderArea import *
from Application import *
from Controleur import *
from Personnage import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.playlist()
        self.initUI()

    def closeEvent(self,event):
        QCoreApplication.instance().quit()

    def initUI(self):
        # Initialise la fenêtre
        self.setWindow()
        # Initialise le Controleur avec 1 joueur par défaut
        self.control=Controleur(1)

        #Création d'un QStackedLayout pour ajouter les différents menus
        self.stackedLayout = QStackedLayout()

        # ajout des menus
        self.stackedLayout.addWidget(self.MainMenu())
        self.stackedLayout.addWidget(self.MenuOptions())
        self.stackedLayout.addWidget(self.MenuNbJoueurs())
        self.stackedLayout.addWidget(self.MenuJeu())
        self.stackedLayout.addWidget(self.MenuPerso(1))
        self.stackedLayout.addWidget(self.ChangeVolume())
        self.stackedLayout.addWidget(self.MenuPerso(2))

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.stackedLayout)
        self.setCentralWidget(self.mainWidget)
        self.setImage()
        self.setCenter()
        self.show()

    #change l'index du stackedLayout pour le menu du choix de perso 1
    def onClickedPerso(self):
        self.stackedLayout.setCurrentIndex(4)

    #change l'index du stackedLayout pour le menu du jeu quand il y a un 1 joueur
    # met la musique sur celle in-game
    def onClicked1P(self):
        self.stackedLayout.setCurrentIndex(3)
        self.playlist.setCurrentIndex(1)

    #change l'index du stackedLayout pour le menu du choix de perso 2
    #et change la valeur de nbPlayer
    def onClicked2P(self):
        self.control.nbPlayer=2
        self.control.renderArea.nbPlayer=2
        self.control.renderArea.updateScore()
        self.update()
        self.stackedLayout.setCurrentIndex(6)


    def choixPerso(self,player,choix):
        # permet d'assigner des perso différents aux autres personnages
        imgNames=["ninja","cowboy","chevalier","indien"]
        imgNames.remove(choix)
        if player==1:
            # assigne les différentes images des persos pour 1 joueur
            self.control.character1.imgName=choix
            self.control.character2.imgName=imgNames[0]
            self.control.character3.imgName=imgNames[1]
            self.control.character4.imgName=imgNames[2]
            # update et change le stackedLayout pour le choix du nombre de Joueurs
            self.control.updateCharacterUrl()
            self.update()
            self.stackedLayout.setCurrentIndex(2)

        else:
            # assigne les différentes images des persos pour 2 joueurs
            self.control.character2.imgName=imgNames[0]
            self.control.character3.imgName=imgNames[1]
            self.control.character4.imgName=choix
            # update
            self.control.updateCharacterUrl()
            self.update()
            # lance la partie et met la musique de jeu
            self.stackedLayout.setCurrentIndex(3)
            self.playlist.setCurrentIndex(1)

    #change l'index du stackedLayout pour le menu option
    def onClickedOption(self):
        self.stackedLayout.setCurrentIndex(1)

    #change l'index du stackedLayout pour le menu du reglage du volume
    def onClickedVolume(self):
        self.stackedLayout.setCurrentIndex(5)

    # change le volume
    def ChangeVolume(self):
        widget = QWidget()
        vLayout = QVBoxLayout()

        # creer un QSlider
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
        slider.setFixedWidth(320)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(5)
        slider.setGeometry(30, 40, 200, 30)
        midWidth = self.frameGeometry().width()/2
        midHeight = self.frameGeometry().height()/2
        slider.move(midWidth - 50,midHeight-50)

        # change le volume de le musique et des sons
        slider.valueChanged.connect(self.music.setVolume)
        slider.valueChanged.connect(self.control.sound.soundPutBomb.setVolume)
        slider.valueChanged.connect(self.control.sound.soundExplosionBomb.setVolume)
        slider.valueChanged.connect(self.control.sound.soundDeathPlayer.setVolume)
        slider.valueChanged.connect(self.control.sound.soundDeathEnemy.setVolume)
        slider.valueChanged.connect(self.control.sound.soundGetBonus.setVolume)

        # bouton retour
        buttonReturn = QPushButton("Retour")

        buttonReturn.clicked.connect(self.onClickedReturn)

        vLayout.addWidget(slider)
        vLayout.addWidget(buttonReturn)

        # ajout d'un style de bouton
        styleSheet = "QPushButton {background : #e85941; border-radius: 10px; font: bold 28px; border-color: white; padding: 6px; margin-right: 10px; margin-top: 20px;}"

        widget.setStyleSheet(styleSheet)

        vLayout.setAlignment(Qt.AlignCenter)

        widget.setLayout(vLayout)

        return widget

    #change l'index du stackedLayout pour le menu principal
    def onClickedReturn(self):
        self.stackedLayout.setCurrentIndex(0)

    def MainMenu(self):
        self.playlist.setCurrentIndex(0)
        self.music.play()
        #création d'un widget et d'un layout
        widget = QWidget()
        vLayout = QVBoxLayout()

        #  calcule la moitié de la taille de la fenêtre pour placer les boutons
        midWidth = self.frameGeometry().width()/2
        midHeight = self.frameGeometry().height()/2

        #Bouton pour lancer le jeu
        buttonJeu = QPushButton("Jouer")
        buttonJeu.move(midWidth - 50,midHeight-50)
        buttonJeu.clicked.connect(self.onClickedPerso)

        # Bouton des options
        buttonOpt = QPushButton("Options")
        buttonOpt.move(midWidth - 50,midHeight)
        buttonOpt.clicked.connect(self.onClickedOption)

        # Bouton pour quitter
        buttonQuit= QPushButton("Quitter")
        buttonQuit.move(midWidth - 50,midHeight+50)
        buttonQuit.clicked.connect(QCoreApplication.instance().quit)

        # ajout les widgets au layout
        vLayout.addWidget(buttonJeu)
        vLayout.addWidget(buttonOpt)
        vLayout.addWidget(buttonQuit)

        # ajout d'un style de bouton
        styleSheet = "QPushButton {background : #e85941; border-radius: 10px; font: bold 28px; border-color: white; padding: 6px; margin-bottom: 10px}"

        widget.setStyleSheet(styleSheet)


        vLayout.setAlignment(Qt.AlignCenter)

        widget.setLayout(vLayout)

        return widget

    def MenuOptions(self):
        self.playlist.setCurrentIndex(0)
        self.music.play()
        # creation d'un widget et layout
        widget = QWidget()
        vLayout = QVBoxLayout()

        # creation de boutons
        buttonVolume = QPushButton("Volume")
        buttonReturn = QPushButton("Retour")

        buttonVolume.clicked.connect(self.onClickedVolume)
        buttonReturn.clicked.connect(self.onClickedReturn)

        # ajout des boutons dans le layout
        vLayout.addWidget(buttonVolume)
        vLayout.addWidget(buttonReturn)

        # ajout d'un style de bouton
        styleSheet = "QPushButton {background : #e85941; border-radius: 10px; font: bold 28px; border-color: white; padding: 6px; margin-right: 10px; margin-bottom: 10px}"

        widget.setStyleSheet(styleSheet)

        vLayout.setAlignment(Qt.AlignCenter)

        widget.setLayout(vLayout)

        return widget

    def MenuPerso(self,player):
        self.playlist.setCurrentIndex(0)
        self.music.play()
        # menu du choix du personnage
        widget = QWidget()
        textWidget=QWidget()
        buttonsWidget=QWidget()

        # layout du text
        hLayout1=QHBoxLayout()

        # label
        text=QLabel("Choisissez votre personnage :")

        # ajout des widgets
        hLayout1.addWidget(text)

        hLayout1.setAlignment(Qt.AlignCenter)
        textWidget.setLayout(hLayout1)

        # layout des boutons
        hLayout2 = QHBoxLayout()

        # icones
        ImgNinja = QIcon('img/personnages/ninja/ninja_menu.png')
        ImgIndien = QIcon('img/personnages/indien/indien_menu.png')
        ImgCowboy = QIcon('img/personnages/cowboy/cowboy_menu.png')
        ImgChevalier = QIcon('img/personnages/chevalier/chevalier_menu.png')

        # boutons de choix des persos
        buttonNinja = QPushButton(ImgNinja, "")
        buttonIndien = QPushButton(ImgIndien ,"")
        buttonChevalier = QPushButton(ImgChevalier ,"")
        buttonCowboy = QPushButton(ImgCowboy ,"")
        buttonReturn = QPushButton("Retour")

        buttonNinja.setIconSize(QSize(250,250))
        buttonIndien.setIconSize(QSize(250,250))
        buttonCowboy.setIconSize(QSize(250,250))
        buttonChevalier.setIconSize(QSize(250,250))

        # quand on clique
        if player==1:
            # si 1 joueur
            # functools.partial(func,param1,etc) permet de passer des paramètre a une fonction
            # ce que ne permet le clicked.connect à la base
            # cela a permis de factoriser le code
            buttonNinja.clicked.connect(functools.partial(self.choixPerso,1,"ninja"))
            buttonIndien.clicked.connect(functools.partial(self.choixPerso,1,"indien"))
            buttonChevalier.clicked.connect(functools.partial(self.choixPerso,1,"chevalier"))
            buttonCowboy.clicked.connect(functools.partial(self.choixPerso,1,"cowboy"))
        else:
            # si 2 joueur
            buttonNinja.clicked.connect(functools.partial(self.choixPerso,2,"ninja"))
            buttonIndien.clicked.connect(functools.partial(self.choixPerso,2,"indien"))
            buttonChevalier.clicked.connect(functools.partial(self.choixPerso,2,"chevalier"))
            buttonCowboy.clicked.connect(functools.partial(self.choixPerso,2,"cowboy"))

        # ajout des boutons dans le layout
        hLayout2.addWidget(buttonNinja)
        hLayout2.addWidget(buttonIndien)
        hLayout2.addWidget(buttonChevalier)
        hLayout2.addWidget(buttonCowboy)

        hLayout2.setAlignment(Qt.AlignCenter)
        buttonsWidget.setLayout(hLayout2)

        # ajout d'un style de bouton
        styleSheet = "QPushButton {background : transparent; border-radius: 10px; font: bold 20px; border-color: white; padding: 10px; margin-right: 20px; margin-bottom: 500px; margin-left: 20px;} QLabel{margin-top: 250px;}"

        widget.setStyleSheet(styleSheet)

        # layout principal
        vLayout=QVBoxLayout()
        # ajout des widget images et boutons
        vLayout.addWidget(textWidget)
        vLayout.addWidget(buttonsWidget)
        vLayout.setSpacing(5)
        widget.setLayout(vLayout)

        return widget

    # Menu demandant le nombre de joueurs
    def MenuNbJoueurs(self):
        self.playlist.setCurrentIndex(0)
        self.music.play()
        # creation du widget
        widget = QWidget()
        vLayout = QVBoxLayout()

        # hLayout des boutons
        widgetButton=QWidget()
        buttonLayout=QHBoxLayout()
        # boutons 1 et 2 joueurs
        self.button1P = QPushButton("1 Joueur")
        self.button2P = QPushButton("2 Joueurs")

        # ajout des boutons
        buttonLayout.addWidget(self.button1P)
        buttonLayout.addWidget(self.button2P)

        # connect la fonction à faire au clique
        self.button1P.clicked.connect(self.onClicked1P)
        self.button2P.clicked.connect(self.onClicked2P)

        widgetButton.setLayout(buttonLayout)

        # creation des widgets avec les infos
        widgetInfo=QWidget()
        widgetInfo2=QWidget()
        InfoLayout=QHBoxLayout()
        InfoLayout2=QHBoxLayout()

        toucheP1=QLabel("Déplacement flèches.\n Bombe : Espace")
        toucheP2=QLabel("Déplacement ZQSD.\n Bombe : A")


        regles=QLabel("Règles: \n Déplacez votre personnage dans la map et explosez des blocs pour obtenir des points, et peut-être des bonus ! \n Le bonus flamme vous permet d'augmenter la portée de votre bombe, qui est d'une case seulement. \n Le bonus bombe augmente le nombre de bombes que vous pouvez poser de 1, pour gagner des points plus rapidement. \n Le bonus coeur augmente votre vie de 1, pour pouvoir survivre à une ou plusieurs explosions. \n Le bonus pièce augmente votre score de 1. \n \n Les points :\n Bloc explosé :  +1 point\n Ennemi tué: +10 points \n Bonus pièce : +1 point")

        # layout et widget des touche
        InfoLayout.addWidget(toucheP1)
        InfoLayout.addWidget(toucheP2)
        widgetInfo.setLayout(InfoLayout)

        # layout et widget des régles
        InfoLayout2.addWidget(regles)
        widgetInfo2.setLayout(InfoLayout2)

        vLayout.addWidget(widgetButton)
        vLayout.addWidget(widgetInfo)
        vLayout.addWidget(widgetInfo2)

        # style
        styleSheet = "QPushButton {background : #e85941; border-radius: 10px; font: bold 28px; border-color: white; padding: 6px; margin-right: 10px;}"

        widget.setStyleSheet(styleSheet)

        vLayout.setAlignment(Qt.AlignCenter)

        widget.setLayout(vLayout)

        return widget

    def MenuJeu(self):
        # ajout de renderArea pour joueur dans le stackedLayout
        widget = QWidget()
        vLayout = QVBoxLayout()

        vLayout.addWidget(self.control.renderArea)

        widget.setLayout(vLayout)
        return widget


    def setImage(self):
        # met l'image de fond d'ecran
        image = QImage("img/Imagefond/Fond_inGame.png")
        size = image.scaled(QSize(self.frameGeometry().width(),self.frameGeometry().height()))

        palette = QPalette()
        palette.setBrush(10,QBrush(size))
        self.setPalette(palette)

    def setCenter(self):
        # Place la fenêtre au milieu de l'écran
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def playlist(self):
        # playlist des musiques du jeu
        self.playlist = QMediaPlaylist()

        url1 = QUrl.fromLocalFile(os.getcwd() +"/sound/menuSound/menu.wav")
        url2 = QUrl.fromLocalFile(os.getcwd() +"/sound/menuSound/map.wav")

        self.playlist.addMedia(QMediaContent(url1))
        self.playlist.addMedia(QMediaContent(url2))

        self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)

        self.music = QMediaPlayer()
        self.music.setPlaylist(self.playlist)

    def setWindow(self):
        width = QDesktopWidget().availableGeometry().width()
        height = QDesktopWidget().availableGeometry().height()
        self.setGeometry(10, 10, width, height)
        self.setWindowTitle("Bomberboy")
        self.statusBar().showMessage("Aucun événement")

    def keyPressEvent(self, event):
        key=event.key()

        # touche joueur1
        if key==Qt.Key_Left:
            self.statusBar().showMessage("Touche gauche")
            # demande au Controleur de deplacer le personnage
            self.control.movePlayer(1,-1,0,"left")
            self.update()
        elif key==Qt.Key_Right:
            self.statusBar().showMessage("Touche droite")
            # demande au Controleur de deplacer le personnage
            self.control.movePlayer(1,1,0,"right")
            self.update()
        elif key==Qt.Key_Up:
            self.statusBar().showMessage("Touche haut")
            # demande au Controleur de deplacer le personnage
            self.control.movePlayer(1,0,-1,"up")
            self.update()
        elif key==Qt.Key_Down:
            self.statusBar().showMessage("Touche bas")
            # demande au Controleur de deplacer le personnage
            self.control.movePlayer(1,0,1,"down")
            self.update()
        elif key==Qt.Key_Space:
            self.control.putBomb(1)
            self.update()

        # touches joueur2
        elif self.control.nbPlayer==2 and key==Qt.Key_Z:
            self.control.movePlayer(4,0,-1,"up")
            self.update()
        elif self.control.nbPlayer==2 and key==Qt.Key_Q:
            self.control.movePlayer(4,-1,0,"left")
            self.update()
        elif self.control.nbPlayer==2 and key==Qt.Key_S:
            self.control.movePlayer(4,0,1,"down")
            self.update()
        elif self.control.nbPlayer==2 and key==Qt.Key_D:
            self.control.movePlayer(4,1,0,"right")
            self.update()
        elif self.control.nbPlayer==2 and key==Qt.Key_A:
            self.control.putBomb(4)
            self.update()

        # touche echap
        elif key==Qt.Key_Escape:
            self.initUI()
            self.onClickedReturn()
            self.playlist.setCurrentIndex(0)
