#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.gui import utils
from prymatex.core.plugin import PMXBaseWidgetComponent, PMXBaseKeyHelper, PMXBaseAddon
from prymatex.core import exceptions

class PMXBaseEditor(PMXBaseWidgetComponent):
    """Every editor should extend this class in order to guarantee it'll be able to be place in tab.
    """
    #tabStatusChanged
    CREATION_COUNTER = 0
    UNTITLED_FILE_TEMPLATE = "Untitled {CREATION_COUNTER}"
    
    def __init__(self):
        PMXBaseWidgetComponent.__init__(self)
        self.filePath = None
        self.project = None
        self.externalAction = None
    
    @property
    def creationCounter(self):
        if not hasattr(self, "_creationCounter"):
            PMXBaseEditor.CREATION_COUNTER += 1
            setattr(self, "_creationCounter", PMXBaseEditor.CREATION_COUNTER)
        return self._creationCounter
    
    def open(self, filePath):
        """ Open file """
        self.application.fileManager.openFile(filePath)
        content = self.application.fileManager.readFile(filePath)
        self.setPlainText(content)
        self.setFilePath(filePath)

    def save(self, filePath):
        """ Save content of editor in a file """
        self.application.fileManager.writeFile(filePath, self.toPlainText())
        if filePath != self.filePath:
            if self.filePath is not None:
                self.application.fileManager.closeFile(self.filePath)
                self.application.fileManager.openFile(filePath)
            self.setFilePath(filePath)
        self.setModified(False)
        self.setExternalAction(None)
    
    def close(self):
        """ Close editor """
        if self.filePath is None and self.creationCounter == PMXBaseEditor.CREATION_COUNTER:
            PMXBaseEditor.CREATION_COUNTER -= 1
        elif self.filePath is not None:
            self.application.fileManager.closeFile(self.filePath)

    def reload(self):
        """ Reload current file """
        content = self.application.fileManager.readFile(self.filePath)
        self.setPlainText(content)
        self.setExternalAction(None)
        
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
            baseIcon = utils.combineIcons(baseIcon, importantIcon, 0.8)
        return baseIcon
    
    def tabTitles(self):
        if self.filePath is not None:
            return self.application.fileManager.fullsplit(self.filePath)[::-1]
        return self.UNTITLED_FILE_TEMPLATE.format(CREATION_COUNTER = self.creationCounter).split()

    def setTabTitle(self, title):
        self._tabTitle = title

    def tabTitle(self):
        if hasattr(self, "_tabTitle"):
            return self._tabTitle
        if self.filePath is not None:
            return self.application.fileManager.basename(self.filePath)
        return self.UNTITLED_FILE_TEMPLATE.format(CREATION_COUNTER = self.creationCounter)

    def tabToolTip(self):
        if self.filePath is not None:
            return self.filePath
        return self.UNTITLED_FILE_TEMPLATE.format(CREATION_COUNTER = self.creationCounter)
    
    def fileDirectory(self):
        return self.application.fileManager.dirname(self.filePath)
    
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
        # FIXME: Rename or move files make produces bogus behavior 
        return self.externalAction == self.application.fileManager.DELETED    

    #============================================================
    # Global navigation api
    #============================================================
    def nextLocation(self):
        return False
        
    def previousLocation(self):
        return False

    def lastLocation(self):
        return False
        
    def locationCount(self):
        return 0

    def resetLocationIndex(self, back = True):
        pass

    #============================================================
    # Cursor positions as tuple
    #============================================================
    def setCursorPosition(self, cursorPosition):
        pass

    def cursorPosition(self):
        return (0, 0)

    def contributeToTabMenu(self):
        ''' When an editor is right clicked on it's tab, the editor
        can provide custom actions to the menu through this callback'''
        return []
    
    def runKeyHelper(self, event):
        return PMXBaseWidgetComponent.runKeyHelper(self, event.key())
        
    #======================================================================
    # For Plugin Manager administrator
    #======================================================================    
    @classmethod
    def acceptFile(cls, filePath, mimetype):
        return True

#======================================================================
# Base Helper
#======================================================================    
class PMXBaseEditorKeyHelper(PMXBaseKeyHelper):
    def accept(self, editor, event):
        return PMXBaseKeyHelper.accept(self, editor, event.key())
    
    def execute(self, editor, event):
        PMXBaseKeyHelper.accept(self, editor, event.key())

#======================================================================
# Base Addon
#======================================================================    
class PMXBaseEditorAddon(PMXBaseAddon):
    def initialize(self, editor):
        PMXBaseAddon.initialize(self, editor)
        self.editor = editor

    def finalize(self):
        pass
