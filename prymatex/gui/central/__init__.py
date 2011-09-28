#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from prymatex.core import exceptions

class PMXBaseTab(object):
    #tabStatusChanged
    
    creation_counter = 0
    def __init__(self, fileInfo = None):
        self.fileInfo = fileInfo

    def setFileInfo(self, fileInfo):
        self.fileInfo = fileInfo
        self.emit(QtCore.SIGNAL("tabStatusChanged()"))
        
    def getTabIcon(self):
        return QtGui.QIcon()
    
    def getTabTitle(self):
        if self.fileInfo is not None:
            return self.fileInfo.fileName()
        elif not hasattr(self, "creation_counter"):
            self.creation_counter = PMXBaseTab.creation_counter
            PMXBaseTab.creation_counter += 1
        return "untitled %d" % self.creation_counter
    
    def isNew(self):
        return self.fileInfo is None
        
    def isEmpty(self):
        return True
        
    def isModified(self):
        return False
    
    def zoomIn(self):
        pass

    def zoomOut(self):
        pass
    
    @classmethod
    def newInstance(cls, fileInfo = None, parent = None):
        return cls(fileInfo, parent)