#! /usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.getcwd() + "/GUI")
sys.path.append(os.getcwd() + "/Objects")
sys.path.append(os.getcwd() + "/robotImages")
sys.path.append(os.getcwd() + "/Robots")
from window import MainWindow, setEXT
from PyQt5.QtWidgets import QApplication
from battle import Battle
global extRUN
extRUN=False

def setextRUN():
    global extRUN
    extRUN=True



def RUN(listORG,listGEN):
    app = QApplication(sys.argv)
    app.setApplicationName("Python-Robocode")
    myapp = MainWindow()
    myapp.show()
    #myapp.on_pushButton_clicked() # spustí last battle  (window)
    #myapp.on_actionNew_triggered() # zobrazí okno pro přidání botů do battlu (window)
    
    if extRUN:
        #custom solution, executed when learning
        #listGEN=["trainingRobot1"]
        #listORG=["coin","demo","generated","charlier","T800","track_target","wall_runner","wall_tt"]
        Battle.setGLOB(True,False,listORG,listGEN) # nastaví, že jde o gen test  Gtest,genTEST
        myapp.on_actionNew_2_triggered() # opens widow with bot selection and adds them all
        setEXT() # close robocode
    else:
         Battle.setGLOB(False,False,listORG,listGEN) # set gen test  Gtest,genTEST  set bot name
    
    sys.exit(app.exec_())
       
