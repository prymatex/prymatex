#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.gui import utils
from prymatex.core.plugin import PMXBaseWidgetPlugin, Key_Any
from prymatex.core import exceptions

class PMXBaseEditor(PMXBaseWidgetPlugin):
    """Every editor should extend this class in order to guarantee it'll be able to be place in tab.
    """
    #tabStatusChanged
    KEY_HELPERS = {}
    CREATION_COUNTER = 0
    UNTITLED_FILE_TEMPLATE = "Untitled {CREATION_COUNTER}"
    
    def __init__(self):
        PMXBaseWidgetPlugin.__init__(self)
        self.filePath = None
        self.project = None
        self.externalAction = None
    
    @property
    def creationCounter(self):
        if not hasattr(self, "_creationCounter"):
            PMXBaseEditor.CREATION_COUNTER += 1
            setattr(self, "_creationCounter", PMXBaseEditor.CREATION_COUNTER)
        return self._creationCounter
    
    def setMainWindow(self, mainWindow):
        self.mainWindow = mainWindow
    
    def open(self, filePath):
        """ Open file """
        content = self.application.fileManager.openFile(filePath)
        self.setPlainText(content)
        self.setFilePath(filePath)

    def save(self, filePath):
        """ Save content of editor in a file """
        self.application.fileManager.saveFile(filePath, self.toPlainText())
        if filePath != self.filePath:
            if self.filePath is not None:
                self.application.fileManager.closeFile(self.filePath)
            self.setFilePath(filePath)
        self.setModified(False)
        self.setExternalAction(None)
        self.showMessage("<i>%s</i> saved" % self.filePath)
    
    def close(self):
        """ Close editor """
        if self.filePath is None and self.creationCounter == PMXBaseEditor.CREATION_COUNTER:
            PMXBaseEditor.CREATION_COUNTER -= 1
        elif self.filePath is not None:
            self.application.fileManager.closeFile(self.filePath)

    def setFilePath(self, filePath):
        self.filePath = filePath
        self.emit(QtCore.SIGNAL("tabStatusChanged()"))
        
    def setProject(self, project):
        self.project = project
        
    def tabIcon(self):
        baseIcon = QtGui.QIcon()
        if self.filePath is not None:
            baseIcon = resources.getIcon(self.filePath)
        if self.isModified():
            baseIcon = resources.getIcon("save")
        if self.externalAction != None:
            importantIcon = resources.getIcon("important")
            baseIcon = utils.combineIcons(baseIcon, importantIcon, 0.6)
        return baseIcon
    
    def tabTitle(self):
        if self.filePath is not None:
            return os.path.basename(self.filePath)
        return self.UNTITLED_FILE_TEMPLATE.format(CREATION_COUNTER = self.creationCounter)
    
    def tabToolTip(self):
        if self.filePath is not None:
            return self.filePath
        return self.UNTITLED_FILE_TEMPLATE.format(CREATION_COUNTER = self.creationCounter)
    
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

    def setExternalAction(self, action):
        self.externalAction = action
        self.emit(QtCore.SIGNAL("tabStatusChanged()"))

    def isExternalChanged(self):
        return self.externalAction == self.application.fileManager.CHANGED

    def isExternalDeleted(self):
        return self.externalAction == self.application.fileManager.DELETED    

    def setCursorPosition(self, cursorPosition):
        pass

    def contributeToTabMenu(self, menu):
        ''' When an editor is right clicked on it's tab, the editor
        can provide custom actions to the menu through this callback'''
        pass
    
    #======================================================================
    # For Plugin Manager administrator
    #======================================================================    
    @classmethod
    def acceptFile(cls, filePath, mimetype):
        return True
        
    @classmethod
    def addKeyHelper(cls, helper):
        helpers = cls.KEY_HELPERS.setdefault(helper.KEY, [])
        helpers.append(helper)
        
    def findHelpers(self, key):
        helpers = self.KEY_HELPERS[Key_Any][:]
        return helpers + self.KEY_HELPERS.get(key, [])