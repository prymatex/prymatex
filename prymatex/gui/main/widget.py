#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject

class PMXBaseWidget(QtGui.QWidget):
    # Signals
    tabStatusChanged = QtCore.pyqtSignal()
    
    def getTitle(self):
        pass
    
    def getIcon(self):
        pass

    def isModified(self):
        return False
    
    def close(self):
        pass
    
    def save(self):
        pass
    
    def saveAs(self):
        pass
    
    def setContent(self):
        pass

    @classmethod
    def factoryMethod(cls, fileInfo):
        pass