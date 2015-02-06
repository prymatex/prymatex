#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers.icons import combine_icons
from prymatex.core import notifier

from prymatex.core.components.base import (PrymatexComponentWidget, PrymatexAddon)

from prymatex.utils.decorators import deprecated

class PrymatexEditor(PrymatexComponentWidget):
    UNTITLED_FILE_TEMPLATE = "Untitled"
    
    def __init__(self, file_path = None, **kwargs):
        super(PrymatexEditor, self).__init__(**kwargs)
        self._file_path = file_path
        self._project = None
        self._external_actions = notifier.NONE
        self._title = self.UNTITLED_FILE_TEMPLATE

    def open(self, file_path):
        """ Open file """
        self.application().fileManager.openFile(file_path)
        self.setFilePath(file_path)

    def save(self, file_path):
        """ Open close file """
        if file_path != self._file_path:
            if self._file_path is not None:
                self.application().fileManager.closeFile(self._file_path)
                self.application().fileManager.openFile(file_path)
            self.setFilePath(file_path)
        self.setModified(False)
        self.setExternalAction(notifier.NONE)
    
    def close(self):
        """ Close editor """
        if self._file_path is not None:
            self.application().fileManager.closeFile(self._file_path)

    def reload(self):
        """ Reload current file """
        self.setModified(False)
        self.setExternalAction(notifier.NONE)

    def project(self):
        return self._project

    def filePath(self):
        return self._file_path
    
    def setFilePath(self, file_path):
        self._file_path = file_path
        self._project = self.application().projectManager.findProjectForPath(self._file_path)
        self._title = self.application().fileManager.basename(file_path)
        self.modificationChanged.emit(False)

    def icon(self):
        baseIcon = QtGui.QIcon()
        if self._file_path is not None:
            baseIcon = self.resources().get_icon(self._file_path)
        if self.isModified():
            baseIcon = self.resources().get_icon("document-save")
        if self._external_actions & notifier.CHANGED:
            importantIcon = self.resources().get_icon("information")
            baseIcon = combine_icons(baseIcon, importantIcon, 0.8)
        return baseIcon
    
    def title(self):
        return self._title

    def tooltip(self):
        return self.hasFile() and self.filePath() or self.title()
    
    def fileDirectory(self):
        return self.application().fileManager.dirname(self._file_path)
    
    def fileName(self):
        return self.application().fileManager.basename(self._file_path)
        
    def fileFilters(self):
        return []
    
    def hasFile(self):
        return bool(self._file_path)
        
    def isEmpty(self):
        return True
    
    def isModified(self):
        return False
    
    def setModified(self, modified):
        pass 
    
    def isReadOnly(self):
        """Returns true if the editor may not be modified."""
        return False
        
    def externalAction(self):
        return self._external_actions
        
    def setExternalAction(self, actions):
        self._external_actions = actions
        self.modificationChanged.emit(False)

    def isExternalChanged(self):
        return self._external_actions & notifier.CHANGED

    def isExternalDeleted(self):
        return self._external_actions & notifier.DELETED   

    #------------ Bundle Item Handler
    def bundleItemHandler(self):
        return None
        
    #------------ Global navigation api
    def saveLocationMemento(self, memento):
        self.newLocationMemento.emit(memento)
        
    def restoreLocationMemento(self, memento):
        pass
    
    def contributeToTabMenu(self):
        ''' When an editor is right clicked on it's tab, the editor
        can provide custom actions to the menu through this callback'''
        return []
    
    # ---------- For Plugin Manager administrator
    @classmethod
    def acceptFile(cls, file_path, mimetype):
        return True

#======================================================================
# Addon
#======================================================================    
class PrymatexEditorAddon(PrymatexAddon):
    def __init__(self, **kwargs):
        super(PrymatexEditorAddon, self).__init__(**kwargs)
        self.editor = kwargs.get("parent")
