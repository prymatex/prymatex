#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.ui.configure.addons import Ui_Addons
from prymatex.models.settings import SettingsTreeNode

def AddonsSettingsWidgetFactory(namespace):
    class AddonsSettingsWidget(SettingsTreeNode, Ui_Addons, QtWidgets.QWidget):
        NAMESPACE = namespace
        
        def __init__(self, component_class, **kwargs):
            super(AddonsSettingsWidget, self).__init__(component_class, nodeName="addons", **kwargs)
            self.setupUi(self)

        def loadSettings(self):
            super(AddonsSettingsWidget, self).loadSettings()
            self.setTitle("Addons")
            self.setIcon(self.application().resources().get_icon("settings-addons"))
    return AddonsSettingsWidget
