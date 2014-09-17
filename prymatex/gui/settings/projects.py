#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.ui.configure.projects import Ui_Projects
from prymatex.models.settings import SettingsTreeNode

class ProjectSettingsWidget(SettingsTreeNode, Ui_Projects, QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super(ProjectSettingsWidget, self).__init__(nodeName = "projects", **kwargs)
        self.setupUi(self)
        self.setTitle("Projects")
        self.setIcon(self.resources().get_icon("settings-project"))

