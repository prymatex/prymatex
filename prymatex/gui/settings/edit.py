#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore
from prymatex import resources

from prymatex.ui.configure.edit import Ui_Edit
from prymatex.models.settings import SettingsTreeNode

class EditSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_Edit):
    NAMESPACE = "editor"
    TITLE = "Edit"
    ICON = resources.getIcon("document-edit")


    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "edit", settingGroup)
        self.setupUi(self)


    def loadSettings(self):
        pass