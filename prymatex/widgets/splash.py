#!/usr/bin/env python

from PyQt4 import QtGui, QtCore


class SplashScreen(QtGui.QSplashScreen):
    def __init__(self, pixmap):
        QtGui.QSplashScreen.__init__(self, pixmap)
        self.defaultAlignment = QtCore.Qt.AlignCenter
        self.defaultColor = QtCore.Qt.black
        self.message = ""
        self.color = self.alignment = None
        # TODO Tomar valores de la imagen
        self.rect = QtCore.QRect(7, 253, 415, 14)
    
    def drawContents(self, painter):
        painter.setPen(self.color or self.defaultColor)
        painter.drawText(self.rect, self.alignment or self.defaultAlignment, self.message)

    def showMessage(self, message, alignment = None, color = None):
        self.message = message
        self.alignment = alignment
        self.color = color
        QtGui.QSplashScreen.showMessage(self, self.message, 
                                              self.alignment or self.defaultAlignment, 
                                              self.color or self.defaultColor)
    
    def setDefaultAlignment(self, alignment):
        self.defaultAlignment = alignment
        
    def setDefaultColor(self, color):
        self.defaultColor = color
        
    def setMessageRect(self, rect):
        self.rect = rect
    