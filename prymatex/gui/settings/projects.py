#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources

from prymatex.ui.configure.projects import Ui_Projects
from prymatex.models.settings import SettingsTreeNode

class ProjectSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_Projects):
    NAMESPACE = "general"
    TITLE = "Projects"
    ICON = resources.getIcon("project-development")
    
    def __init__(self, settingGroup, profile = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "projects", settingGroup, profile)
        self.setupUi(self)