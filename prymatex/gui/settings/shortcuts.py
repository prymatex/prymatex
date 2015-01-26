#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.ui.configure.shortcuts import Ui_Shortcuts
from prymatex.models.settings import SettingsTreeNode

class ShortcutsSettingsWidget(SettingsTreeNode, Ui_Shortcuts, QtWidgets.QWidget):
    """Environment variables"""
    NAMESPACE = "general"

    def __init__(self, **kwargs):
        super(ShortcutsSettingsWidget, self).__init__(nodeName = "shortcuts", **kwargs)
        self.setupUi(self)
        self.setTitle("Shortcuts")
        self.setIcon(self.resources().get_icon("settings-shortcuts"))
        self.shortcutsTreeModel = self.application().shortcutsTreeModel
        self.configTreeView()
        self.configActivation()

    def configTreeView(self):
        self.treeViewShortcuts.setModel(self.shortcutsTreeModel)
        self.treeViewShortcuts.setAnimated(True)
        self.treeViewShortcuts.selectionModel().selectionChanged.connect(
            self.on_treeViewShortcuts_selectionChanged
        )

    def configActivation(self):
        self.lineEditShortcut.installEventFilter(self)
        
    def loadSettings(self):
        super(ShortcutsSettingsWidget, self).loadSettings()

    def currentShortcut(self):
        return self.shortcutsTreeModel.node(self.treeViewShortcuts.currentIndex())
        
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj == self.lineEditShortcut:
            sequence = QtGui.QKeySequence(int(event.modifiers()) + event.key())
            self.currentShortcut().setKeySequence(sequence)
            self.lineEditShortcut.setText(sequence.toString())
            return True
        return super(ShortcutsSettingsWidget, self).eventFilter(obj, event)

    def on_treeViewShortcuts_selectionChanged(self, selected, deselected):
        if selected.indexes():
            index = selected.indexes()[0]
            node = self.shortcutsTreeModel.node(index)
            sequence = node.keySequence()
            self.lineEditShortcut.setEnabled(sequence is not None)
            self.lineEditShortcut.setText(sequence and sequence.toString() or "")