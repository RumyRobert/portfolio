# -*- coding: utf-8 -*-

"""
Module implementing Battle.
"""

import os
import pickle

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot

from robot import Robot
from Ui_battle import Ui_Dialog

class Battle(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def setGLOB(Gtest1,genTEST1,listORG1,listGEN1):
        global Gtest,genTEST,listORG,listGEN
        Gtest=Gtest1
        genTEST=genTEST1
        listORG=listORG1
        listGEN=listGEN1

    def __init__(self, parent = None):
        """
        Constructor
        """
        

        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.window = parent
        botnames = []
        self.listBots = {}
        botFiles = os.listdir(os.getcwd() + "/Robots") #načte ostré roboty z disku
        if genTEST:
            botFiles.extend( os.listdir(os.getcwd() + "/Robots/t")) #načte generované roboty z disku
        
        for botFile in botFiles:
            if botFile.endswith('.py'):
                botName = botPath =  botFile[:botFile.rfind('.')]
                if botName not in botnames:
                    botnames.append(botName)
                    try:
                        botModule =  __import__(botPath)
                        for name in dir(botModule):
                            if getattr(botModule,  name) in Robot.__subclasses__():
                                someBot = getattr(botModule, name)
                                bot = someBot
                                self.listBots[str(bot).replace("<class '","").replace("'>", "")] = bot
                                break
                    except Exception as e:
                        print("Problem with bot file '{}': {}".format(botFile, str(e)))

                        
        for key in self.listBots.keys():
            self.listWidget.addItem(key)
        
        if Gtest ==True: #----------------------------------------------            
            #listORG=["coin","demo","generated","charlier","T800","track_target","wall_runner","wall_tt"]
            for i in self.listBots:
                #print(i)
                if str(i).split(".")[0] in listORG or str(i).split(".")[0] in listGEN :
                    self.listWidget_2.addItem(i)    
            
            
        width = self.spinBox.value()
        height = self.spinBox_2.value()
        botList = []
        
        for i in range(self.listWidget_2.count()):

            key = str(self.listWidget_2.item(i).text())
            botList.append(self.listBots[key])

        #print("botlist: ",botList) # [<class 'charlier.Charlier'>, <class 'coin.Camper'>, <class 'demo.Demo'>, <class 'T800.T800'>, <class 'target.Target'>, <class 'track_target.TargetTracker'>, <class 'wall_runner.WallRunner'>, <class 'wall_tt.WallTargetTracker'>]
        #print("BOTS",self.listBots )
        self.save(width, height, botList)
        self.window.setUpBattle(width, height, botList)





        
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Add Bot
        """                
        self.listWidget_2.addItem(self.listWidget.currentItem().text())
    
      


    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Remove Bot
        """
        item = self.listWidget_2.takeItem(self.listWidget_2.currentRow())
        item = None
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Start
        """
        width = self.spinBox.value()
        height = self.spinBox_2.value()
        botList = []
        
        for i in range(self.listWidget_2.count()):

            key = str(self.listWidget_2.item(i).text())
            botList.append(self.listBots[key])
        
        #print(botList) # [<class 'charlier.Charlier'>, <class 'coin.Camper'>, <class 'demo.Demo'>, <class 'T800.T800'>, <class 'target.Target'>, <class 'track_target.TargetTracker'>, <class 'wall_runner.WallRunner'>, <class 'wall_tt.WallTargetTracker'>]
        self.save(width, height, botList)
        self.window.setUpBattle(width, height, botList)   

        
    def save(self, width, height, botList):
        dico = {}
        dico["width"] = width
        dico["height"] = height
        dico["botList"] = botList

        if not os.path.exists(os.getcwd() + "/.datas/"):
            os.makedirs(os.getcwd() + "/.datas/")
        
        with open(os.getcwd() + "/.datas/lastArena",  'wb') as file:
            pickler = pickle.Pickler(file)
            pickler.dump(dico)
        file.close()      