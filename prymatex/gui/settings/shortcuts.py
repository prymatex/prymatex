#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import keyevent_to_keysequence
from prymatex.qt.compat import getOpenFileName, getSaveFileName

from prymatex.core import config

from prymatex.utils import json

from prymatex.ui.configure.shortcuts import Ui_Shortcuts
from prymatex.models.settings import SettingsTreeNode

class ShortcutsSettingsWidget(SettingsTreeNode, Ui_Shortcuts, QtWidgets.QWidget):
    """Environment variables"""
    NAMESPACE = "general"

    def __init__(self, component_class, **kwargs):
        super(ShortcutsSettingsWidget, self).__init__(component_class, nodeName="shortcuts", **kwargs)
        self.setupUi(self)
        self.lineEditShortcut.installEventFilter(self)

    def configTreeView(self):
        self.treeViewShortcuts.setModel(self.shortcutsTreeModel)
        self.treeViewShortcuts.setAnimated(True)
        self.treeViewShortcuts.selectionModel().selectionChanged.connect(
            self.on_treeViewShortcuts_selectionChanged
        )

    def loadSettings(self):
        super(ShortcutsSettingsWidget, self).loadSettings()
        self.setTitle("Shortcuts")
        self.setIcon(self.application().resources().get_icon("settings-shortcuts"))
        self.shortcutsTreeModel = self.application().resourceManager.shortcutsTreeModel
        self.configTreeView()

    def currentShortcut(self):
        return self.shortcutsTreeModel.node(self.treeViewShortcuts.currentIndex())
        
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj == self.lineEditShortcut:
            if self.lineEditShortcut.hasSelectedText():
                self.lineEditShortcut.clear()
            sequence = keyevent_to_keysequence(event, prefix=self.lineEditShortcut.text())
            if sequence:
                self.currentShortcut().setKeySequence(sequence)
                self.lineEditShortcut.setText(sequence.toString())
            return True
        return super(ShortcutsSettingsWidget, self).eventFilter(obj, event)

    def on_treeViewShortcuts_selectionChanged(self, selected, deselected):
        if selected.indexes():
            index = selected.indexes()[0]
            node = self.shortcutsTreeModel.node(index)
            # TODO Mejorar esto del _isproxy
            self.lineEditShortcut.setEnabled(not node._isproxy)
            self.lineEditShortcut.setText(node.toString())
            self.lineEditShortcut.selectAll()
            self.lineEditShortcut.setFocus()
    
    def _set_shortcuts_to_settings(self):
        shortcuts = self.shortcutsTreeModel.dictionary()
        self.settings().set('shortcuts', shortcuts)
        
    # ---------- AUTOCONNECT: Button Export
    def on_pushButtonExport_pressed(self):
        selected_path, selected_filter = getSaveFileName(
            self,
            caption="Export shortcuts",
            basedir=config.USER_HOME_PATH
        )
        if selected_path:
            shortcuts = self.shortcutsTreeModel.dictionary(defaults=True)
            json.write_file(shortcuts, selected_path)

    def on_pushButtonImport_pressed(self):
        selected_path, selected_filter = getOpenFileName(
            self,
            caption="Import shortcuts",
            basedir=config.USER_HOME_PATH
        )
        if selected_path:
            shortcuts = json.read_file(selected_path)
            print(shortcuts)
            
    def on_pushButtonResetAll_pressed(self):
        for shortcut in self.shortcutsTreeModel.shortcuts():
            shortcut.resetKeySequence()
        self._set_shortcuts_to_settings()
        
