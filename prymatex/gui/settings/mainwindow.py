#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.mainwindow import Ui_MainWindow
from prymatex.models.settings import SettingsTreeNode

class MainWindowSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_MainWindow):
    TITLE = "Main Window"
    NAMESPACE = "general"
    ICON = resources.getIcon("preferences-system-windows-actions")
    
    def __init__(self, settingGroup, profile = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "mainwindow", settingGroup, profile)
        self.setupUi(self)
