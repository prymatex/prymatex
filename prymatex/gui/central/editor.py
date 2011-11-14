#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from prymatex.core import exceptions

class PMXBaseEditor(object):
    '''
    Every editor should extend this class in order to guarantee it'll be able
    to be place in tab.
    '''
    #tabStatusChanged
    
    creation_counter = 0
    def __init__(self):
        self.fileInfo = None
        self.project = None
        self.creation_counter = PMXBaseEditor.creation_counter
        PMXBaseEditor.creation_counter += 1
        
    def setFileInfo(self, fileInfo):
        self.fileInfo = fileInfo
        self.emit(QtCore.SIGNAL("tabStatusChanged()"))
        
    def getTabIcon(self):
        return QtGui.QIcon()
    
    def getTabTitle(self):
        if self.fileInfo is not None:
            return self.fileInfo.fileName()
        return "untitled %d" % self.creation_counter
    
    def isNew(self):
        return self.fileInfo is None
        
    def isEmpty(self):
        return True
        
    def isModified(self):
        return False
    
    def setModified(self, modified):
        pass
    
    def setCursorPosition(self, cursorPosition):
        pass
    
    @classmethod
    def newInstance(cls, application, fileInfo = None, parent = None):
        return cls(fileInfo, parent)
    
    def showMessage(self, message, timeout = None, icon = None):
        raise NotImplementedError("You need to extend PMXMessageOverlay")