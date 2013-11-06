#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex import resources
from prymatex.models.settings import SettingsTreeNode
from prymatex.widgets.multidicteditor import MultiDictTableEditorWidget

class ShortcutsSettingsWidget(MultiDictTableEditorWidget, SettingsTreeNode):
    """Environment variables"""
    NAMESPACE = "general"
    TITLE = "Shortcuts"
    ICON = resources.getIcon("code-variable")

    def __init__(self, settingGroup, profile = None, parent = None):
        MultiDictTableEditorWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "shortcuts", settingGroup, profile)

    def loadSettings(self):
        print(self.settingGroup)

    def on_model_dictionaryChanged(self, dictionaryName):
        data = self.model().dumpData(dictionaryName)
        data = [{"variable": item[0],
            "value": item[1],
            "enabled": item[2]} for item in data]
        print(data)