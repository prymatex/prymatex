#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.addons import Ui_Addons
from prymatex.models.settings import SettingsTreeNode

def AddonsSettingsWidgetFactory(namespace):
    class AddonsSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_Addons):
        TITLE = "Addons"
        NAMESPACE = namespace
        ICON = resources.getIcon("preferences-plugin")
        
        def __init__(self, settingGroup, profile = None, parent = None):
            QtGui.QWidget.__init__(self, parent)
            SettingsTreeNode.__init__(self, "addons", settingGroup, profile)
            self.setupUi(self)
    return AddonsSettingsWidget