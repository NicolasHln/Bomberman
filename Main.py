#! /usr/bin/python3
# -*- coding: utf-8 -*-
#

import sys
#Dis d'importer les fichier dans le dossier code
sys.path.insert(0,'code/')
from Window import *
from Application import *

app = Application(sys.argv)
win = Window()
sys.exit(app.exec_())
