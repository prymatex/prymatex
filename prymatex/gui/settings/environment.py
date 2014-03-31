#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex import resources
from prymatex.models.settings import SettingsTreeNode
from prymatex.widgets.multidicteditor import MultiDictTableEditorWidget

class VariablesSettingsWidget(SettingsTreeNode, MultiDictTableEditorWidget):
    """Environment variables"""
    NAMESPACE = "general"
    TITLE = "Variables"
    ICON = resources.get_icon("code-variable")

    def __init__(self, **kwargs):
        super(VariablesSettingsWidget, self).__init__(nodeName = "environment", **kwargs)
        self.model().dictionaryChanged.connect(self.on_model_dictionaryChanged)

    def loadSettings(self):
        super(VariablesSettingsWidget, self).loadSettings()
        values = [ (value["variable"], value["value"], value["enabled"]) 
            for value in self.settings.value("shellVariables")]
        self.addTuples('user', values, editable = True, selectable=True)
        self.addDictionary('prymatex', self.application.supportManager.environment)
        self.addDictionary('system', os.environ, visible = False)

    def on_model_dictionaryChanged(self, dictionaryName):
        data = self.model().dumpData(dictionaryName)
        data = [{"variable": item[0],
            "value": item[1],
            "enabled": item[2]} for item in data]
        self.settings.setValue("shellVariables", data)
