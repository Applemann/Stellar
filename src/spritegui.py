#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Emilio Coppola
#
# This file is part of Stellar.
#
# Stellar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Stellar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License


import sys
import os
import os.path
import shutil
from PyQt4.Qt import Qt
from PyQt4 import QtGui, QtCore
from PIL import Image




class SpriteGUI(QtGui.QWidget):
  
    def __init__(self, main, icon, dirname):
        super(SpriteGUI, self).__init__()
        self.main = main
        self.dirname = dirname
        self.icon = icon
        self.initUI()
                        
    def initUI(self):
        self.image_file = os.path.join(self.dirname, "Sprites/%s.png"%(self.icon))
        img = Image.open(self.image_file)
        width, height = img.size
        extension = os.path.splitext(self.image_file)[1][1:]
        Format  = str(extension)
        frames = 1

        #Groupbox Container-----------------------------------
        self.ContainerGrid = QtGui.QGridLayout(self.main)
        self.ContainerGrid.setMargin (0)
        
                
        self.BtnOK = QtGui.QPushButton('OK')
        self.BtnOK.setGeometry (32,32,32,32)
        self.BtnOK.setIcon(QtGui.QIcon('Data/accept.png'))

        #Scroll Area------------------------------------------
        self.sprite = QtGui.QPixmap(os.path.join(self.dirname, "Sprites/%s.png"%(self.icon)))
                                    
        
        self.spriteLbl = QtGui.QLabel(self.main)
        self.spriteLbl.setPixmap(self.sprite)
        self.spriteLbl.setAlignment(QtCore.Qt.AlignTop)
        self.spriteLbl.setText("caca")
                                    
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidget(self.spriteLbl)
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.mousePressEvent = self.pixelSelect
        self.click_positions = []
        
        self.scrollArea.setWidgetResizable(True)
        
        
        #Groupbox General-------------------------------------
        self.GeneralBox = QtGui.QWidget()
        self.layout = QtGui.QGridLayout()		
        self.NameAndThingsBox = QtGui.QFrame() 
        
		
        self.BtnLoad = QtGui.QPushButton('Load Sprite')
        self.BtnLoad.setIcon(QtGui.QIcon('Data/folder.png'))
        self.BtnLoad.clicked.connect(self.LoadSprite)

        self.BtnSave = QtGui.QPushButton('Save Sprite')
        self.BtnSave.setIcon(QtGui.QIcon('Data/save.png'))
        self.BtnSave.clicked.connect(self.SaveSprite)
 
        self.BtnEdit = QtGui.QPushButton('Edit Sprite')
        self.BtnEdit.setIcon(QtGui.QIcon('Data/editbutton.png'))
        self.BtnEdit.clicked.connect(self.EditSprite)

        self.LblName = QtGui.QLabel('Name:') 
        self.qleSprite = QtGui.QLineEdit("%s"%(self.icon))
        
        self.NameFrame = QtGui.QFrame()
        
        self.namelayout = QtGui.QGridLayout()
        self.namelayout.setMargin (0)
        self.namelayout.addWidget(self.LblName,0,0)
        self.namelayout.addWidget(self.qleSprite,0,1)
        
        self.NameFrame.setLayout(self.namelayout)


        self.OriginBox = QtGui.QGroupBox("Origin")
        self.LblX = QtGui.QLabel('X:')
        self.LblY = QtGui.QLabel('Y:') 
        self.EdirXorig = QtGui.QLineEdit("0")
        self.EdirYorig = QtGui.QLineEdit("0")

        self.originlayout = QtGui.QGridLayout()
        self.originlayout.addWidget(self.LblX,7,0)
        self.originlayout.addWidget(self.EdirXorig,7,1)
        self.originlayout.addWidget(self.LblY,7,2)
        self.originlayout.addWidget(self.EdirYorig,7,3)
        
        self.OriginBox.setLayout(self.originlayout)

        self.Lblspacer = QtGui.QLabel(" ")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)



        self.LblWidth = QtGui.QLabel('Width:   %d Pixels'%(width)) 
 
        self.LblHeight = QtGui.QLabel('Height:  %d Pixels'%(height))
        
        self.LblSubimages = QtGui.QLabel('Number of subimages: %d'%(frames))

        self.LblFormat = QtGui.QLabel('File Format:  %s'%(Format)) 


	self.nameandlayout = QtGui.QGridLayout()
        self.nameandlayout.addWidget(self.NameFrame,0,0)	
        self.nameandlayout.addWidget(self.Lblspacer,1,0)
        self.nameandlayout.addWidget(self.BtnLoad,1,0)
        self.nameandlayout.addWidget(self.BtnSave,2,0)
        self.nameandlayout.addWidget(self.BtnEdit,3,0)
        self.nameandlayout.addWidget(self.LblWidth,4,0)
        self.nameandlayout.addWidget(self.LblHeight,5,0)
        self.nameandlayout.addWidget(self.LblSubimages,6,0)
        self.nameandlayout.addWidget(self.OriginBox,8,0)
        
        self.NameAndThingsBox.setLayout(self.nameandlayout)

		
        self.layout.addWidget(self.NameAndThingsBox)
        self.layout.addItem(spacerItem)
        self.layout.addWidget(self.BtnOK)
		
        self.GeneralBox.setMaximumWidth (170)
        self.GeneralBox.setLayout(self.layout)
		
        self.ContainerGrid.setSpacing(0)
		
        self.spritesplitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        self.spritesplitter.addWidget(self.GeneralBox)
        self.spritesplitter.addWidget(self.scrollArea)
        self.ContainerGrid.addWidget(self.spritesplitter)
        
	
	
    def pixelSelect(self, event):
        self.click_positions.append(event.pos())
        pen = QtGui.QPen(QtCore.Qt.red)
        line = str(self.click_positions)
        positions = line.replace(')', '(')
        positions = positions.replace(',', '(')
        positions = positions.replace(' ', '')
        lista = positions.split('(')
        self.xorig = lista[1]
        self.yorig = lista[2]
        self.EdirXorig.setText(self.xorig)
        self.EdirYorig.setText(self.yorig)
        for point in self.click_positions:
            self.scene.addLine(point.x(), point.y(), 2, 2, pen)
        self.click_positions = []

        
    def LoadSprite(self):
        self.asprite = QtGui.QFileDialog.getOpenFileNames(self, 'Open Sprite(s)', 
                '', self.tr("Image file (*.png *.gif *.jpg)"))
        
        if self.asprite !='':
            for sprite in self.asprite:
                shutil.copy(sprite, self.image_file)
                self.sprite = QtGui.QPixmap(sprite)
                self.spriteLbl.setPixmap(self.sprite)
                self.image_file = os.path.join(self.dirname, "Sprites/%s.png"%(self.icon))
                img = Image.open(self.image_file)
                width, height = img.size
                extension = os.path.splitext(self.image_file)[1][1:]
                Format  = str(extension)
                self.LblWidth.setText('Width:   %d Pixels'%(width))
                self.LblHeight.setText('Height:  %d Pixels'%(height))
                self.LblFormat.setText('File Format:  %s'%(Format))
                

    def SaveSprite(self):
        self.fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Sprite(s)', 
                '', self.tr("Image file (*.png)"))

        if self.fname !='':
            shutil.copy(self.image_file, self.fname)


    def EditSprite(self):
        os.startfile(self.image_file)#TO BE DONE :)
        

