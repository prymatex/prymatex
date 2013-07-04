#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.general import Ui_General
from prymatex.models.settings import SettingsTreeNode


class GeneralSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_General):
    TITLE = "General"
    ICON = resources.getIcon("preferences-other")

    def __init__(self, settingGroup, profile = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "general", settingGroup, profile)
        self.setupUi(self)

    def loadSettings(self):
        SettingsTreeNode.loadSettings(self)
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

        checks = ( self.checkBoxAskAboutExternalDeletions, self.checkBoxAskAboutExternalChanges )
        [ check.blockSignals(True) for check in checks ]
        self.checkBoxAskAboutExternalDeletions.setChecked(self.settingGroup.value('askAboutExternalDeletions'))
        self.checkBoxAskAboutExternalChanges.setChecked(self.settingGroup.value('askAboutExternalChanges'))
        [ check.blockSignals(False) for check in checks ]

    @QtCore.Slot(int)
    def on_checkBoxAskAboutExternalDeletions_stateChanged(self, state):
        self.settingGroup.setValue('askAboutExternalDeletions', state == QtCore.Qt.Checked)
        
    @QtCore.Slot(int)
    def on_checkBoxAskAboutExternalChanges_stateChanged(self, state):
        self.settingGroup.setValue('askAboutExternalChanges', state == QtCore.Qt.Checked)
        
    @QtCore.Slot(str)
    def on_comboBoxQtStyle_activated(self, styleName):
        self.settingGroup.setValue('qtStyle', styleName)

    @QtCore.Slot(str)
    def on_comboBoxQtStyleSheet_activated(self, styleSheetName):
        self.settingGroup.setValue('qtStyleSheet', styleSheetName)
