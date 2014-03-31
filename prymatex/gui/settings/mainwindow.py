#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.mainwindow import Ui_MainWindow
from prymatex.models.settings import SettingsTreeNode

class MainWindowSettingsWidget(SettingsTreeNode, Ui_MainWindow, QtGui.QWidget):
    TITLE = "Main Window"
    NAMESPACE = "general"
    ICON = resources.get_icon("preferences-system-windows-actions")
    
    def __init__(self, **kwargs):
        super(MainWindowSettingsWidget, self).__init__(nodeName = "mainwindow", **kwargs)
        self.setupUi(self)
    
    def loadSettings(self):
        super(MainWindowSettingsWidget, self).loadSettings()
        self.checkBoxShowTabsIfMoreThanOne.setChecked(self.settings.value("showTabsIfMoreThanOne", False))

    @QtCore.Slot(bool)
    def on_checkBoxShowTabsIfMoreThanOne_clicked(self, checked):
        self.settings.setValue('showTabsIfMoreThanOne', self.checkBoxShowTabsIfMoreThanOne.isChecked())
