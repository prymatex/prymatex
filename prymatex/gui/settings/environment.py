#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui

from prymatex import resources
from prymatex.models.settings import SettingsTreeNode
from prymatex.widgets.multidicteditor import MultiDictTableEditorWidget
from prymatex.models.environment import EnvironmentTableModel

class PMXEnvVariablesWidget(MultiDictTableEditorWidget, SettingsTreeNode):
    """Environment variables
    """
    NAMESPACE = "general"
    TITLE = "Variables"
    ICON = resources.getIcon("code-variable")
    
    def __init__(self, settingGroup, profile = None, parent = None):
        MultiDictTableEditorWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "environment", settingGroup, profile)
        self.setupUi(self)
    
    def loadSettings(self):
        self.addDictionary('user', self.application.supportManager.shellVariables, editable = True, selectable=True)
        self.addDictionary('prymatex', self.application.supportManager.environment)
        self.addDictionary('system', os.environ, visible = False)
    
    def on_variablesModel_userVariablesChanged(self, group, variables):
        self.settingGroup.setValue('shellVariables', variables)

    def on_pushAdd_pressed(self):
        self.model.insertVariable()
        
    def on_pushRemove_pressed(self):
        index = self.tableViewVariables.currentIndex()
        self.model.removeRows(index.row() , 1)