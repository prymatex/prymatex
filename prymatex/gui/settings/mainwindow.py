#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.mainwindow import Ui_Mainwindow
from prymatex.models.settings import SettingsTreeNode

class MainWindowSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_Mainwindow):
    TITLE = "Main Window"
    NAMESPACE = "general"
    ICON = resources.getIcon("preferences-other")
    
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "mainwindow", settingGroup)
        self.setupUi(self)
