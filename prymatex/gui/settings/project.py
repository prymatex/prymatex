#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources

from prymatex.models.settings import SettingsTreeNode

class ProjectSettingsWidget(QtGui.QWidget, SettingsTreeNode):
    TITLE = "Project"
    ICON = resources.getIcon("project-development")
    
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "project", settingGroup)