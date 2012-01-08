#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PyQt4 import QtGui, QtCore

from prymatex.core.plugin import PMXBasePlugin
from prymatex.core import exceptions

class PMXBaseEditor(PMXBasePlugin):
    """
    Every editor should extend this class in order to guarantee it'll be able to be place in tab.
    """
    #tabStatusChanged
    HELPERS = {}
    CREATION_COUNTER = 0
    UNTITLED_FILE_TEMPLATE = "Untitled {CREATION_COUNTER}"
    
    def __init__(self, filePath = None, project = None):
        self.filePath = filePath
        self.project = project
        if self.filePath is None:
            PMXBaseEditor.CREATION_COUNTER += 1
            self.creation_counter = PMXBaseEditor.CREATION_COUNTER
    
    def saved(self, filePath):
        if filePath != self.filePath:
            self.setFilePath(filePath)
        self.setModified(False)
        self.showMessage("<i>%s</i> saved" % self.filePath)
    
    def closed(self):
        if self.filePath is None and self.creation_counter == PMXBaseEditor.CREATION_COUNTER:
            PMXBaseEditor.CREATION_COUNTER -= 1
        elif self.filePath is not None:
            self.application.fileManager.closeFile(self.filePath)

    def setFilePath(self, filePath):
        self.filePath = filePath
        self.emit(QtCore.SIGNAL("tabStatusChanged()"))
        
    def setProject(self, project):
        self.project = project
        
    def tabIcon(self):
        return QtGui.QIcon()
    
    def tabTitle(self):
        if self.filePath is not None:
            return os.path.basename(self.filePath)
        return self.UNTITLED_FILE_TEMPLATE.format(CREATION_COUNTER = self.creation_counter)
    
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
    
    def checkExternalModification(self):
        if self.isNew():
            return False
        return self.application.fileManager.checkExternalModification(self.filePath, self.mtime)
    
    def showMessage(self, message, timeout = None, icon = None):
        raise NotImplementedError("You need to extend PMXMessageOverlay")
    
    def contributeToTabMenu(self, menu):
        ''' When an editor is right clicked on it's tab, the editor
        can provide custom actions to the menu through this callback'''
        pass
    
    #======================================
    #Editor Helpers
    #======================================
    @classmethod
    def addKeyHelper(cls, helper):
        helpers = cls.HELPERS.setdefault(helper.KEY, [])
        helpers.append(helper)
        
    def findHelpers(self, key):
        helpers = self.HELPERS[Key_Any][:]
        return helpers + self.HELPERS.get(key, [])

Key_Any = 0        
class PMXBaseKeyHelper(PMXBasePlugin):
    KEY = Key_Any
    def accept(self, editor, event, cursor = None, scope = None):
        return event.key() == self.KEY
    
    def execute(self, editor, event, cursor = None, scope = None):
        pass