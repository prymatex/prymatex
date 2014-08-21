#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.ui.configure.mainwindow import Ui_MainWindow
from prymatex.models.settings import SettingsTreeNode

class MainWindowSettingsWidget(SettingsTreeNode, Ui_MainWindow, QtGui.QWidget):
    NAMESPACE = "general"
        
    def __init__(self, **kwargs):
        super(MainWindowSettingsWidget, self).__init__(nodeName = "mainwindow", **kwargs)
        self.setupUi(self)
        self.setTitle("Main Window")
        self.setIcon(self.resources().get_icon("preferences-system-windows-actions"))

    def loadSettings(self):
        super(MainWindowSettingsWidget, self).loadSettings()
        self.checkBoxShowTabsIfMoreThanOne.setChecked(self.settings.value("showTabsIfMoreThanOne", False))

    @QtCore.Slot(bool)
    def on_checkBoxShowTabsIfMoreThanOne_clicked(self, checked):
        self.settings.setValue('showTabsIfMoreThanOne', self.checkBoxShowTabsIfMoreThanOne.isChecked())
