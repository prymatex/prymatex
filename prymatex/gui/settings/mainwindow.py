#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore, QtWidgets

from prymatex.ui.configure.mainwindow import Ui_MainWindow
from prymatex.models.settings import SettingsTreeNode

class MainWindowSettingsWidget(SettingsTreeNode, Ui_MainWindow, QtWidgets.QWidget):
    NAMESPACE = "general"
    
    def __init__(self, component_class, **kwargs):
        super(MainWindowSettingsWidget, self).__init__(component_class, nodeName="mainwindow", **kwargs)
        self.setupUi(self)

    def loadSettings(self):
        super(MainWindowSettingsWidget, self).loadSettings()
        self.setTitle("Main Window")
        self.setIcon(self.application().resources().get_icon("settings-main-window"))
        self.checkBoxShowTabsIfMoreThanOne.setChecked(self.settings().get("showTabsIfMoreThanOne", False))

    @QtCore.Slot(bool)
    def on_checkBoxShowTabsIfMoreThanOne_clicked(self, checked):
        self.settings().set('show_tabs_if_more_than_one', self.checkBoxShowTabsIfMoreThanOne.isChecked())
    
    @QtCore.Slot(str)
    def on_comboBoxTitleTemplate_activated(self, template):
        self.settings().set('window_title_template', template)