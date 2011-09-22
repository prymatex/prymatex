#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

class PMXBaseTab(object):
    creation_counter = 0
    def __init__(self):
        self.fileInfo = None
        self.creation_counter = PMXBaseTab.creation_counter
        PMXBaseTab.creation_counter += 1
    
    def updateTabStatus(self):
        self.splitter.setActiveIcon(self, self.getTabIcon())
        self.splitter.setWidgetTitle(self, self.getTabTitle())
    
    def setFileInfo(self, fileInfo):
        self.fileInfo = fileInfo
        self.updateTabStatus()

    def setSplitter(self, splitter):
        self.splitter = splitter
        self.updateTabStatus()

    def getTabIcon(self):
        return QtGui.QIcon()
    
    def getTabTitle(self):
        if self.fileInfo is not None:
            return self.fileInfo.fileName()
        return "untitled %d" % self.creation_counter
    
    def isModified(self):
        return False
    
    def close(self):
        pass
        
    def open(self, fileInfo):
        self.setFileInfo(fileInfo)
    
    def save(self, fileInfo):
        self.setFileInfo(fileInfo)