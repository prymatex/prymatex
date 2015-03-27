#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.models.properties import PropertyTreeNode
from prymatex.widgets.multidicteditor import MultiDictTableEditorWidget

class EnvironmentPropertiesWidget(PropertyTreeNode, MultiDictTableEditorWidget):
    """Environment variables"""
    NAMESPACE = ""
    def __init__(self, **kwargs):
        super(EnvironmentPropertiesWidget, self).__init__(nodeName="environment", **kwargs)
        self.setTitle("Variables")
        self.project = None
        self.model().dictionaryChanged.connect(self.on_model_dictionaryChanged)
        
    def acceptFileSystemItem(self, fileSystemItem):
        return fileSystemItem.isProject()
    
    def edit(self, project):
        self.project = project
        self.clear()
        variables = [ (value["variable"], value["value"], value["enabled"])
            for value in self.project.shell_variables or []]
        self.addTuples('user', variables, editable = True, selectable=True)
        self.addDictionary('project', self.project.variables)
        self.addDictionary('prymatex', self.application().supportManager.environmentVariables(), visible = False)

    def on_model_dictionaryChanged(self, dictionaryName):
        variables = self.model().dumpData(dictionaryName)
        variables = [{"variable": item[0], 
            "value": item[1], 
            "enabled": item[2]} for item in variables]
        self.project.shellVariables = variables
