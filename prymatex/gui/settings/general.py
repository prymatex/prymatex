#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.general import Ui_General
from prymatex.models.settings import SettingsTreeNode

class GeneralSettingsWidget(SettingsTreeNode, Ui_General, QtGui.QWidget):
    TITLE = "General"
    ICON = resources.get_icon("preferences-other")

    def __init__(self, **kwargs):
        super(GeneralSettingsWidget, self).__init__(nodeName = "general", **kwargs)
        self.setupUi(self)

    def loadSettings(self):
        super(GeneralSettingsWidget, self).loadSettings()
        currentStyleName = self.settings.value('qtStyle')
        currentStyleSheetName = self.settings.value('qtStyleSheet')
        currentIconTheme = self.settings.value('iconTheme')
        resources = self.application().resources()
        for index, styleName in enumerate(QtGui.QStyleFactory.keys()):
            self.comboBoxQtStyle.addItem(styleName, styleName)
            if currentStyleName and styleName == currentStyleName:
                self.comboBoxQtStyle.setCurrentIndex(index)

        for index, styleSheetName in enumerate(resources.get_stylesheets().keys()):
            self.comboBoxQtStyleSheet.addItem(styleSheetName, styleSheetName)
            if currentStyleSheetName and styleSheetName == currentStyleSheetName:
                self.comboBoxQtStyleSheet.setCurrentIndex(index)

        for index, theme in enumerate(resources.get_themes().values()):
            self.comboBoxIconTheme.addItem(theme.name, theme.name)
            if currentIconTheme and theme.name == currentIconTheme:
                self.comboBoxIconTheme.setCurrentIndex(index)

        checks = ( self.checkBoxAskAboutExternalDeletions, self.checkBoxAskAboutExternalChanges )
        [ check.blockSignals(True) for check in checks ]
        self.checkBoxAskAboutExternalDeletions.setChecked(self.settings.value('askAboutExternalDeletions'))
        self.checkBoxAskAboutExternalChanges.setChecked(self.settings.value('askAboutExternalChanges'))
        [ check.blockSignals(False) for check in checks ]

    @QtCore.Slot(int)
    def on_checkBoxAskAboutExternalDeletions_stateChanged(self, state):
        self.settings.setValue('askAboutExternalDeletions', state == QtCore.Qt.Checked)
        
    @QtCore.Slot(int)
    def on_checkBoxAskAboutExternalChanges_stateChanged(self, state):
        self.settings.setValue('askAboutExternalChanges', state == QtCore.Qt.Checked)
        
    @QtCore.Slot(str)
    def on_comboBoxQtStyle_activated(self, styleName):
        self.settings.setValue('qtStyle', styleName)

    @QtCore.Slot(str)
    def on_comboBoxQtStyleSheet_activated(self, styleSheetName):
        self.settings.setValue('qtStyleSheet', styleSheetName)
        
    @QtCore.Slot(str)
    def on_comboBoxIconTheme_activated(self, iconThemeName):
        self.settings.setValue('iconTheme', iconThemeName)
