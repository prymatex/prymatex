#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.ui.configure.projects import Ui_Projects
from prymatex.models.settings import SettingsTreeNode

class ProjectSettingsWidget(SettingsTreeNode, Ui_Projects, QtWidgets.QWidget):
    def __init__(self, component_class, **kwargs):
        super(ProjectSettingsWidget, self).__init__(component_class, nodeName="projects", **kwargs)
        self.setupUi(self)

    def loadSettings(self):
        super(ProjectSettingsWidget, self).loadSettings()

        self.setTitle("Projects")
        self.setIcon(self.application().resources().get_icon("settings-project"))

