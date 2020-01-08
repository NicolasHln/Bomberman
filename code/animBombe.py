import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Fichier qui a servi a tester de faire l'animation de la bombe que l'on à pas reussi a implémenter en jeu
# pour faire charger  les images le fichier est à lancer dans le /code

class Bomb(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Bomb, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.label = QLabel()
        self.setCentralWidget(self.label)
        self.label.move(500,500)

        self.feu=2
        self.imgFeu="../img/bombe/Explosion_milieu.png"
        self.imgBout="../img/bombe/Explosion_bout.png"
        #la liste pixmapsBombe contient les différentes images qui illustrent la bombe pendant l'animation
        self.pixmapsBombe = ["../img/bombe/bombe1.png","../img/bombe/bombe2.png","../img/bombe/bombe3.png","../img/bombe/bombe4.png","../img/bombe/bombe5.png","../img/bombe/Explosion_centre.png",]
        self._iter_pixmap = iter(self.pixmapsBombe)
        timer = QtCore.QTimer(self, timeout=self.explosion, interval=800)
        timer.start()

    def explosion(self): #l'image va changer d'iteration après un interval 800 jusqu'à la fin de pixmapsBombe
        try:
            img_path = next(self._iter_pixmap)
            pixmap = QPixmap(img_path)
            self.label.setPixmap(pixmap)
        except StopIteration:
            if isinstance(self.sender(), QtCore.QTimer):
                self.sender().stop()



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    b = Bomb()
    b.show()
    sys.exit(app.exec_())
