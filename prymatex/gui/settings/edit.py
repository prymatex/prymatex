#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.ui.configure.edit import Ui_Edit
from prymatex.models.settings import SettingsTreeNode

class EditSettingsWidget(SettingsTreeNode, Ui_Edit, QtWidgets.QWidget):
    NAMESPACE = "editor"

    def __init__(self, **kwargs):
        super(EditSettingsWidget, self).__init__(nodeName = "edit", **kwargs)
        self.setupUi(self)
        self.setTitle("Edit")
        self.setIcon(self.resources().get_icon("settings-edit"))

    def loadSettings(self):
        super(EditSettingsWidget, self).loadSettings()

        self.spinBoxIndentationWidth.setValue(self.settings.get("indentationWidth"))
        self.spinBoxWordLengthToComplete.setValue(self.settings.get("wordLengthToComplete"))

        self.checkBoxRemoveTrailingSpaces.setChecked(self.settings.get("removeTrailingSpaces"))
        self.checkBoxAutoBrackets.setChecked(self.settings.get("autoBrackets"))
        self.checkBoxSmartHomeSmartEnd.setChecked(self.settings.get("smartHomeSmartEnd"))
        self.checkBoxEnableAutoCompletion.setChecked(self.settings.get("enableAutoCompletion"))
        self.checkBoxAdjustIndentationOnPaste.setChecked(self.settings.get("adjustIndentationOnPaste"))
        self.radioButtonSpaces.setChecked(self.settings.get("indentUsingSpaces"))
        self.radioButtonTabulators.setChecked(not self.settings.get("indentUsingSpaces"))

    @QtCore.Slot(bool)
    def on_checkBoxRemoveTrailingSpaces_clicked(self, checked):
        self.settings.set('removeTrailingSpaces', self.checkBoxRemoveTrailingSpaces.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxAutoBrackets_clicked(self, checked):
        self.settings.set('autoBrackets', self.checkBoxAutoBrackets.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxSmartHomeSmartEnd_clicked(self, checked):
        self.settings.set('smartHomeSmartEnd', self.checkBoxSmartHomeSmartEnd.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxEnableAutoCompletion_clicked(self, checked):
        self.settings.set('enableAutoCompletion', self.checkBoxEnableAutoCompletion.isChecked())

    @QtCore.Slot(bool)
    def on_radioButtonSpaces_clicked(self, checked):
        self.settings.set('indentUsingSpaces', checked)

    @QtCore.Slot(bool)
    def on_checkBoxAdjustIndentationOnPaste_clicked(self, checked):
        self.settings.set('adjustIndentationOnPaste', self.checkBoxAdjustIndentationOnPaste.isChecked())

    @QtCore.Slot(int)
    def on_spinBoxIndentationWidth_valueChanged(self, value):
        self.settings.set('indentationWidth', value)

    @QtCore.Slot(int)
    def on_spinBoxWordLengthToComplete_valueChanged(self, value):
        self.settings.set('wordLengthToComplete', value)
