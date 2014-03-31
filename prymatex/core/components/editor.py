#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers.icons import combine_icons

from prymatex.core import exceptions
from prymatex.core.components.base import (PrymatexComponentWidget, 
    PrymatexKeyHelper, PrymatexAddon, Key_Any)

from prymatex import resources

class PrymatexEditor(PrymatexComponentWidget):
    CREATION_COUNTER = 0
    UNTITLED_FILE_TEMPLATE = "Untitled {CREATION_COUNTER}"
    
    def __init__(self, **kwargs):
        super(PrymatexEditor, self).__init__(**kwargs)
    
    def initialize(self, parent = None, **kwargs):
        super(PrymatexEditor, self).initialize(**kwargs)
        self.mainWindow = parent
        self.filePath = None
        self.project = None
        self.externalAction = None
        if not hasattr(self, "modificationChanged"):
            self.modificationChanged = QtCore.Signal(bool)
    
    @property
    def creationCounter(self):
        if not hasattr(self, "_creationCounter"):
            PrymatexEditor.CREATION_COUNTER += 1
            setattr(self, "_creationCounter", PrymatexEditor.CREATION_COUNTER)
        return self._creationCounter
    
    def open(self, filePath):
        """ Open file """
        self.application.fileManager.openFile(filePath)
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
        if self.filePath is None and self.creationCounter == PrymatexEditor.CREATION_COUNTER:
            PrymatexEditor.CREATION_COUNTER -= 1
        elif self.filePath is not None:
            self.application.fileManager.closeFile(self.filePath)

    def reload(self):
        """ Reload current file """
        self.setModified(False)
        self.setExternalAction(None)
        
    def setFilePath(self, filePath):
        self.filePath = filePath
        self.project = self.application.projectManager.findProjectForPath(filePath)
        self.modificationChanged.emit(False)

    def tabIcon(self):
        baseIcon = QtGui.QIcon()
        if self.filePath is not None:
            baseIcon = resources.get_icon(self.filePath)
        if self.isModified():
            baseIcon = resources.get_icon("document-save")
        if self.externalAction is not None:
            importantIcon = resources.get_icon("emblem-important")
            baseIcon = combine_icons(baseIcon, importantIcon, 0.8)
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
        self.modificationChanged.emit(False)

    def isExternalChanged(self):
        return self.externalAction == self.application.fileManager.CHANGED

    def isExternalDeleted(self):
        # FIXME: Rename or move files make produces bogus behavior 
        return self.externalAction == self.application.fileManager.DELETED    

    #------------ Bundle Item Handler
    def bundleItemHandler(self):
        return None
        
    #------------ Global navigation api
    def saveLocationMemento(self, memento):
        # TODO Ver que va a pasar con esto de emitir señales y no heredar de qobject
        self.emit(QtCore.SIGNAL("newLocationMemento"), memento)
        
    def restoreLocationMemento(self, memento):
        pass
    
    #------------ Cursor positions as tuple
    def setCursorPosition(self, cursorPosition):
        pass

    def cursorPosition(self):
        return (0, 0)

    def contributeToTabMenu(self):
        ''' When an editor is right clicked on it's tab, the editor
        can provide custom actions to the menu through this callback'''
        return []
    
    # ---------- For Plugin Manager administrator
    @classmethod
    def acceptFile(cls, filePath, mimetype):
        return True

#======================================================================
# Key Helper
#======================================================================    
class PrymatexEditorKeyHelper(PrymatexKeyHelper):
    def initialize(self, parent = None, **kwargs):
        super(PrymatexEditorKeyHelper, self).initialize(**kwargs)
        self.editor = parent

#======================================================================
# Addon
#======================================================================    
class PrymatexEditorAddon(PrymatexAddon):
    def initialize(self, parent = None, **kwargs):
        super(PrymatexEditorAddon, self).initialize(**kwargs)
        self.editor = parent

