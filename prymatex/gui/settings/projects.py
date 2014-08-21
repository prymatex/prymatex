#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.ui.configure.projects import Ui_Projects
from prymatex.models.settings import SettingsTreeNode

class ProjectSettingsWidget(SettingsTreeNode, Ui_Projects, QtGui.QWidget):
    NAMESPACE = "general"
    
    def __init__(self, **kwargs):
        super(ProjectSettingsWidget, self).__init__(nodeName = "projects", **kwargs)
        self.setupUi(self)
        self.setTitle("Projects")
        self.setIcon(self.resources().get_icon("project-development"))

