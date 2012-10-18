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
        self.setExternalAction(None)
        
    def setFilePath(self, filePath):
        self.filePath = filePath
        self.project = self.application.projectManager.findProjectForPath(filePath)
        self.emit(QtCore.SIGNAL("tabStatusChanged()"))
        
    def tabIcon(self):
        baseIcon = QtGui.QIcon()
        if self.filePath is not None:
            baseIcon = resources.getIcon(self.filePath)
        if self.isModified():
            baseIcon = resources.getIcon("document-save")
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
    # Bundle Item Handler
    #============================================================
    def bundleItemHandler(self):
        return None
        
    #============================================================
    # Global navigation api
    #============================================================
    def saveLocationMemento(self, memento):
        # TODO Ver que va a pasar con esto de emitir señales y no heredar de qobject
        self.emit(QtCore.SIGNAL("newLocationMemento"), memento)
        
    def restoreLocationMemento(self, memento):
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
        runHelper = False
        for helper in self.findHelpers(event.key()):
            runHelper = helper.accept(event)
            if runHelper:
                helper.execute(event)
                break
        return runHelper
        
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
    def initialize(self, editor):
        PMXBaseKeyHelper.initialize(self, editor)
        self.editor = editor

    def accept(self, event):
        return PMXBaseKeyHelper.accept(self, event.key())
    
    def execute(self, event):
        PMXBaseKeyHelper.accept(self, event.key())

#======================================================================
# Base Addon
#======================================================================    
class PMXBaseEditorAddon(PMXBaseAddon):
    def initialize(self, editor):
        PMXBaseAddon.initialize(self, editor)
        self.editor = editor

    def finalize(self):
        pass
