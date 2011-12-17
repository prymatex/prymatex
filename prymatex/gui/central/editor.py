#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PyQt4 import QtGui, QtCore
from prymatex.core import exceptions

class PMXBaseEditor(object):
    """
    Every editor should extend this class in order to guarantee it'll be able
    to be place in tab.
    """
    #tabStatusChanged
    
    creation_counter = 0
    def __init__(self):
        self.filePath = None
        self.project = None
        self.creation_counter = PMXBaseEditor.creation_counter
        PMXBaseEditor.creation_counter += 1
        
    def setFilePath(self, filePath):
        self.filePath = filePath
        self.emit(QtCore.SIGNAL("tabStatusChanged()"))
        
    def setProject(self, project):
        self.project = project
        
    def tabIcon(self):
        return QtGui.QIcon()
    
    UNTITLED_FILE_TEMPLATE = "Untitled {creation_counter}"
    def tabTitle(self):
        if self.filePath is not None:
            return os.path.basename(self.filePath)
        return self.UNTITLED_FILE_TEMPLATE.format(creation_counter = self.creation_counter)
    
    def fileDirectory(self):
        return self.application.fileManager.getDirectory(self.filePath)
    
    def fileName(self):
        return self.tabTitle()
        
    def fileFilters(self):
        return []
    
    def isNew(self):
        return self.filePath is None
        
    def isEmpty(self):
        return True
        
    def isModified(self):
        return False
    
    def setModified(self, modified):
        pass
    
    def setCursorPosition(self, cursorPosition):
        pass
    
    @classmethod
    def newInstance(cls, application, filePath = None, parent = None):
        return cls(filePath, parent)
    
    def showMessage(self, message, timeout = None, icon = None):
        raise NotImplementedError("You need to extend PMXMessageOverlay")