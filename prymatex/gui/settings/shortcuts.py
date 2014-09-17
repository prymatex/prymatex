#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.models.settings import SettingsTreeNode

class ShortcutsSettingsWidget(SettingsTreeNode, QtWidgets.QWidget):
    """Environment variables"""
    NAMESPACE = "general"

    def __init__(self, **kwargs):
        super(ShortcutsSettingsWidget, self).__init__(nodeName = "shortcuts", **kwargs)
        self.setupUi(self)
        self.setTitle("Shortcuts")
        self.setIcon(self.resources().get_icon("settings-shortcuts"))

    def setupUi(self, Shortcuts):
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Shortcuts)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(QtCore.QMargins(0,0,0,0))
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEditFilter = QtWidgets.QLineEdit(Shortcuts)
        self.lineEditFilter.setReadOnly(True)
        self.lineEditFilter.setObjectName("lineEditFilter")
        self.verticalLayout_2.addWidget(self.lineEditFilter)
        self.treeViewShortcuts = QtWidgets.QTreeView(Shortcuts)
        self.treeViewShortcuts.setObjectName("treeViewShortcuts")
        self.verticalLayout_2.addWidget(self.treeViewShortcuts)
        QtCore.QMetaObject.connectSlotsByName(Shortcuts)

    def loadSettings(self):
        super(ShortcutsSettingsWidget, self).loadSettings()
        self.treeViewShortcuts.setModel(self.application().shortcutsTreeModel)
