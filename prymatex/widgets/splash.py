#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self, pixmap):
        super(SplashScreen, self).__init__(pixmap)
        self.defaultAlignment = QtCore.Qt.AlignCenter
        self.defaultColor = QtCore.Qt.black
        self.shadowColor = QtGui.QColor(QtCore.Qt.black)
        self.shadowColor.setAlpha(128)
        self.message = ""
        self.color = self.alignment = None
        
        self.textRect = QtCore.QRect(self.rect().x() + 100, self.rect().y() + 510, 260, 50)
        self.shadowTextRect = QtCore.QRect(self.rect().x() + 101, self.rect().y() + 511, 260, 50)

    def drawContents(self, painter):
        #painter.fillRect(self.textRect, QtCore.Qt.red) test rect text
        painter.setPen(self.shadowColor)
        painter.drawText(self.shadowTextRect, self.alignment or self.defaultAlignment, self.message)
        painter.setPen(self.color or self.defaultColor)
        painter.drawText(self.textRect, self.alignment or self.defaultAlignment, self.message)

    def showMessage(self, message, alignment = None, color = None):
        self.message = message
        self.alignment = alignment
        self.color = color
        QtWidgets.QSplashScreen.showMessage(self, self.message, 
                                              self.alignment or self.defaultAlignment, 
                                              self.color or self.defaultColor)
        
    def setDefaultColor(self, color):
        self.defaultColor = color
    
