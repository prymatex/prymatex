#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.models.properties import PropertyTreeNode
from prymatex.widgets.multidicteditor import MultiDictTableEditorWidget
from prymatex.models.environment import EnvironmentTableModel

class EnvironmentPropertiesWidget(MultiDictTableEditorWidget, PropertyTreeNode):
    """Environment variables"""
    NAMESPACE = ""
    TITLE = "Enviroment Variables"
    def __init__(self, parent = None):
        MultiDictTableEditorWidget.__init__(self, parent)
        PropertyTreeNode.__init__(self, "environment")
        self.project = None
        self.model().dictionaryChanged.connect(self.on_model_dictionaryChanged)
        
    def acceptFileSystemItem(self, fileSystemItem):
        return fileSystemItem.isproject
    
    def edit(self, project):
        self.project = project
        self.clear()
        variables = map(lambda value: {"name": value["variable"],
            "value": value["value"],
            "selected": value["enabled"]
        }, self.project.shellVariables or [])
        
        self.addDictionary('user', variables, editable = True, selectable=True)
        self.addDictionary('project', self.project.environment())
        self.addDictionary('prymatex', self.application.supportManager.environmentVariables(), visible = False)

    def on_model_dictionaryChanged(self, dictionaryName):
        variables = self.model().dictionaryData(dictionaryName, raw = True)
        variables = map(lambda item: {"variable": item["name"], 
            "value": item["value"], 
            "enabled": item["selected"]}, variables)
        self.project.shellVariables = variables