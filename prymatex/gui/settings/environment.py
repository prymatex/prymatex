#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.models.settings import SettingsTreeNode
from prymatex.widgets.multidicteditor import MultiDictTableEditorWidget

class VariablesSettingsWidget(SettingsTreeNode, MultiDictTableEditorWidget):
    NAMESPACE = "general"
    def __init__(self, **kwargs):
        super(VariablesSettingsWidget, self).__init__(nodeName = "environment", **kwargs)
        self.model().dictionaryChanged.connect(self.on_model_dictionaryChanged)
        self.setTitle("Variables")
        self.setIcon(self.resources().get_icon("settings-variables"))

    def loadSettings(self):
        super(VariablesSettingsWidget, self).loadSettings()
        values = [ (value["variable"], value["value"], value["enabled"]) 
            for value in self.settings.get("shellVariables")]
        self.addTuples('user', values, editable=True, selectable=True)
        self.addDictionary('prymatex', self.application().environmentVariables())
        self.addDictionary('system', os.environ, visible = False)

    def on_model_dictionaryChanged(self, dictionaryName):
        data = self.model().dumpData(dictionaryName)
        data = [{"variable": item[0],
            "value": item[1],
            "enabled": item[2]} for item in data]
        self.settings.set("shellVariables", data)
