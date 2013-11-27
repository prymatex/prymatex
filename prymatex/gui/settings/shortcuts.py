#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

import os

from prymatex import resources
from prymatex.models.settings import SettingsTreeNode

class ShortcutsSettingsWidget(QtGui.QWidget, SettingsTreeNode):
    """Environment variables"""
    NAMESPACE = "general"
    TITLE = "Shortcuts"
    ICON = resources.getIcon("configure-shortcuts")

    def __init__(self, settingGroup, profile = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "shortcuts", settingGroup, profile)
        self.setupUi(self)
        
    def setupUi(self, Shortcuts):
        self.verticalLayout_2 = QtGui.QVBoxLayout(Shortcuts)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEditFilter = QtGui.QLineEdit(Shortcuts)
        self.lineEditFilter.setReadOnly(True)
        self.lineEditFilter.setObjectName("lineEditFilter")
        self.verticalLayout_2.addWidget(self.lineEditFilter)
        self.treeViewShortcuts = QtGui.QTreeView(Shortcuts)
        self.treeViewShortcuts.setObjectName("treeViewShortcuts")
        self.verticalLayout_2.addWidget(self.treeViewShortcuts)
        QtCore.QMetaObject.connectSlotsByName(Shortcuts)

    def loadSettings(self):
        self.treeViewShortcuts.setModel(self.application.shortcutsTreeModel)
