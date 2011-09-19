#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject

class PMXBaseWidget(QtGui.QWidget, PMXObject):
    # Signals
    tabStatusChanged = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        super(QtGui.QWidget, self).__init__(parent)
        self.content = self.title = ''
        self.icon = None
        self.modified = False
    
    def close(self):
        pass
    
    def open(self, fileInfo):
        self.content = self.application.fileManager.openFile(fileInfo)
        self.fileInfo = fileInfo

    def save(self):
        fileInfo = self.fileInfo
        newFile = fileInfo is None or not fileInfo.exists()
        if newFile:
            fileInfo = self.application.fileManager.getSaveFile(fileInfo = fileInfo, title = "Save file")
        if fileInfo is not None:
            self.application.fileManager.saveFile(fileInfo, self.content)
            self.modified = False
            self.fileInfo = fileInfo
    
    def saveAs(self):
        fileInfo = self.fileInfo
        fileInfo = self.application.fileManager.getSaveFile(fileInfo = fileInfo, title = "Save file as")
        if fileInfo is not None:
            self.application.fileManager.saveFile(fileInfo, self.content)
            self.modified = False
            self.fileInfo = fileInfo

    @classmethod
    def factoryMethod(cls, fileInfo = None, parent = None):
        instance = cls(parent)
        if fileInfo != None:
            instance.open(fileInfo)
        return instance