#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui
from prymatex.core.components import PMXBaseDialog

from prymatex.widgets.multidicteditor import MultiDictTableEditorWidget

class EnvironmentDialog(QtGui.QDialog, PMXBaseDialog):
    def __init__(self, parent):
        """docstring for __init__"""
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setObjectName("EnvironmentDialog")
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(0)
        self.multiDictTableEditorWidget = MultiDictTableEditorWidget(self)
        self.multiDictTableEditorWidget.setObjectName("multiDictTableEditorWidget")
        self.verticalLayout.addWidget(self.multiDictTableEditorWidget)
        self.setWindowTitle("Environment")
        
    def editEnvironment(self, environment, **kwargs):
        self.multiDictTableEditorWidget.clear()
        self.multiDictTableEditorWidget.addDictionary('environment', environment, editable = True)
        # Add extra dicts
        for name, value in kwargs.items():
            self.multiDictTableEditorWidget.addDictionary(name, value, editable=False)
        self.exec_()
        return self.multiDictTableEditorWidget.dictionaryData("environment")