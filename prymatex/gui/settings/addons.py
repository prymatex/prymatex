#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.addons import Ui_Addons
from prymatex.models.settings import SettingsTreeNode

def AddonsSettingsWidgetFactory(namespace):
    class AddonsSettingsWidget(SettingsTreeNode, Ui_Addons, QtGui.QWidget):
        TITLE = "Addons"
        NAMESPACE = namespace
        ICON = resources.getIcon("preferences-plugin")
        
        def __init__(self, **kwargs):
            super(AddonsSettingsWidget, self).__init__(nodeName = "addons", **kwargs)
            self.setupUi(self)
    return AddonsSettingsWidget