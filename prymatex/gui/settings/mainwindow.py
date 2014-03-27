#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.mainwindow import Ui_MainWindow
from prymatex.models.settings import SettingsTreeNode

class MainWindowSettingsWidget(SettingsTreeNode, Ui_MainWindow, QtGui.QWidget):
    TITLE = "Main Window"
    NAMESPACE = "general"
    ICON = resources.getIcon("preferences-system-windows-actions")
    
    def __init__(self, settingGroup, profile = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "mainwindow", settingGroup, profile)
        self.setupUi(self)
    
    def loadSettings(self):
        SettingsTreeNode.loadSettings(self)
        self.checkBoxShowTabsIfMoreThanOne.setValue(self.settingGroup.value("showTabsIfMoreThanOne", False))
        
    @QtCore.Slot(bool)
    def on_checkBoxShowTabsIfMoreThanOne_clicked(self, checked):
        self.settingGroup.setValue('showTabsIfMoreThanOne', self.checkBoxShowTabsIfMoreThanOne.isChecked())
