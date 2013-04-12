#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui

from prymatex import resources
from prymatex.models.settings import SettingsTreeNode
from prymatex.widgets.multidicteditor import MultiDictTableEditorWidget

class VariablesSettingsWidget(MultiDictTableEditorWidget, SettingsTreeNode):
    """Environment variables"""
    NAMESPACE = "general"
    TITLE = "Variables"
    ICON = resources.getIcon("code-variable")
    
    def __init__(self, settingGroup, profile = None, parent = None):
        MultiDictTableEditorWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "environment", settingGroup, profile)
        self.model().dictionaryChanged.connect(self.on_model_dictionaryChanged)
        
    def loadSettings(self):
        values = map(lambda value: {"name": value["variable"],
            "value": value["value"],
            "selected": value["enabled"]
        }, self.settingGroup.value("shellVariables"))
        self.addDictionary('user', values, editable = True, selectable=True)
        self.addDictionary('prymatex', self.application.supportManager.environment)
        self.addDictionary('system', os.environ, visible = False)

    def on_model_dictionaryChanged(self, dictionaryName):
        data = self.model().dictionaryData(dictionaryName, raw = True)
        data = map(lambda item: {"variable": item["name"], 
            "value": item["value"], 
            "enabled": item["selected"]}, data)
        self.settingGroup.setValue("shellVariables", data)
