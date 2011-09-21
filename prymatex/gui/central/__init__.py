#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject

class PMXBaseTab(PMXObject):
    # Signals
    tabStatusChanged = QtCore.pyqtSignal()
    
    creation_counter = 0
    def __init__(self):
        self.fileInfo = None
        self.modified = False
        self.creation_counter = PMXBaseTab.creation_counter
        PMXBaseTab.creation_counter += 1
        self.title = "untitled %d" % self.creation_counter
    
    def updateTabStatus(self):
        if self.fileInfo != None:
            self.splitter.setActiveIcon(self, self.application.fileManager.getFileIcon(self.fileInfo))
            self.splitter.setWidgetTitle(self, self.fileInfo.fileName())
    
    def setFileInfo(self, fileInfo):
        self.fileInfo = fileInfo
        self.updateTabStatus()

    def setSplitter(self, splitter):
        self.splitter = splitter
        self.updateTabStatus()

    def close(self):
        pass
        
    def open(self, fileInfo):
        self.content = self.application.fileManager.openFile(fileInfo)
        self.setFileInfo(fileInfo)

    def save(self):
        fileInfo = self.fileInfo
        newFile = fileInfo is None or not fileInfo.exists()
        if newFile:
            fileInfo = self.application.fileManager.getSaveFile(fileInfo = fileInfo, title = "Save file")
        if fileInfo is not None:
            self.application.fileManager.saveFile(fileInfo, self.content)
            self.modified = False
            self.setFileInfo(fileInfo)
    
    def saveAs(self):
        fileInfo = self.fileInfo
        fileInfo = self.application.fileManager.getSaveFile(fileInfo = fileInfo, title = "Save file as")
        if fileInfo is not None:
            self.application.fileManager.saveFile(fileInfo, self.content)
            self.modified = False
            self.setFileInfo(fileInfo)

    @classmethod
    def factoryMethod(cls, fileInfo = None, parent = None):
        instance = cls(parent)
        if fileInfo != None:
            instance.open(fileInfo)
        return instance