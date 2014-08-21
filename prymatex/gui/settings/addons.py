#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.ui.configure.addons import Ui_Addons
from prymatex.models.settings import SettingsTreeNode

def AddonsSettingsWidgetFactory(namespace):
    class AddonsSettingsWidget(SettingsTreeNode, Ui_Addons, QtGui.QWidget):
        NAMESPACE = namespace
        
        def __init__(self, **kwargs):
            super(AddonsSettingsWidget, self).__init__(nodeName = "addons", **kwargs)
            self.setupUi(self)
            self.setTitle("Addons")
            self.setIcon(self.resources().get_icon("settings-addons"))
    return AddonsSettingsWidget
