#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.general import Ui_General
from prymatex.models.settings import SettingsTreeNode


class GeneralSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_General):
    TITLE = "General"
    ICON = resources.getIcon("preferences-other")


    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "general", settingGroup)
        self.setupUi(self)


    def loadSettings(self):
        currentStyleName = self.settingGroup.value('qtStyle')
        currentStyleSheetName = self.settingGroup.value('qtStyleSheet')
        for index, styleName in enumerate(QtGui.QStyleFactory.keys()):
            self.comboBoxQtStyle.addItem(styleName, styleName)
            if currentStyleName and styleName == currentStyleName:
                self.comboBoxQtStyle.setCurrentIndex(index)

        for index, styleSheetName in enumerate(resources.STYLESHEETS.keys()):
            self.comboBoxQtStyleSheet.addItem(styleSheetName, styleSheetName)
            if currentStyleSheetName and styleSheetName == currentStyleSheetName:
                self.comboBoxQtStyleSheet.setCurrentIndex(index)
                

    @QtCore.pyqtSlot(str)
    def on_comboBoxQtStyle_activated(self, styleName):
        self.settingGroup.setValue('qtStyle', styleName)


    @QtCore.pyqtSlot(str)
    def on_comboBoxQtStyleSheet_activated(self, styleSheetName):
        self.settingGroup.setValue('qtStyleSheet', styleSheetName)
