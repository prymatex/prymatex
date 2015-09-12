#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers.icons import combine_icons

from prymatex.core.components.base import (PrymatexComponentWidget, PrymatexAddon)

from prymatex.utils.decorators import deprecated

class PrymatexEditor(PrymatexComponentWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__external_action = None

    def open(self, file_path):
        pass

    def save(self, file_path):
        pass
    
    def close(self):
        pass

    def reload(self):
        pass

    def fileFilters(self):
        return []
            
    def isEmpty(self):
        return True
    
    def isReadOnly(self):
        """Returns true if the editor may not be modified."""
        return False
        
    def externalAction(self):
        return self.__external_action
        
    def setExternalAction(self, action):
        self.__external_action = action

    #------------ Bundle Item Handler
    def bundleItemHandler(self):
        return None
        
    #------------ Global navigation api
    def saveLocationMemento(self, memento):
        pass
        #self.newLocationMemento.emit(memento)
        
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
