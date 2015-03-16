#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.ui.configure.general import Ui_General
from prymatex.models.settings import SettingsTreeNode

class GeneralSettingsWidget(SettingsTreeNode, Ui_General, QtWidgets.QWidget):
    def __init__(self, component_class, **kwargs):
        super(GeneralSettingsWidget, self).__init__(component_class, nodeName="general", **kwargs)
        self.setupUi(self)

    def loadSettings(self):
        super(GeneralSettingsWidget, self).loadSettings()
        self.setTitle("General")
        self.setIcon(self.application().resources().get_icon("settings-general"))
        currentStyleName = self.settings().get('qt_style')
        currentStyleSheetName = self.settings().get('qt_style_sheet')
        currentIconTheme = self.settings().get('icon_theme')
        resources = self.application().resources()
        for index, styleName in enumerate(QtWidgets.QStyleFactory.keys()):
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
        self.checkBoxAskAboutExternalDeletions.setChecked(self.settings().get('askAboutExternalDeletions'))
        self.checkBoxAskAboutExternalChanges.setChecked(self.settings().get('askAboutExternalChanges'))
        [ check.blockSignals(False) for check in checks ]

    @QtCore.Slot(int)
    def on_checkBoxAskAboutExternalDeletions_stateChanged(self, state):
        self.settings().set('askAboutExternalDeletions', state == QtCore.Qt.Checked)
        
    @QtCore.Slot(int)
    def on_checkBoxAskAboutExternalChanges_stateChanged(self, state):
        self.settings().set('askAboutExternalChanges', state == QtCore.Qt.Checked)
        
    @QtCore.Slot(str)
    def on_comboBoxQtStyle_activated(self, styleName):
        self.settings().set('qt_style', styleName)

    @QtCore.Slot(str)
    def on_comboBoxQtStyleSheet_activated(self, styleSheetName):
        self.settings().set('qt_style_sheet', styleSheetName)
        
    @QtCore.Slot(str)
    def on_comboBoxIconTheme_activated(self, iconThemeName):
        self.settings().set('icon_theme', iconThemeName)

