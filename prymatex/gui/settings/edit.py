#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore
from prymatex import resources

from prymatex.ui.configure.edit import Ui_Edit
from prymatex.models.settings import SettingsTreeNode

class EditSettingsWidget(SettingsTreeNode, Ui_Edit, QtGui.QWidget):
    NAMESPACE = "editor"
    TITLE = "Edit"
    ICON = resources.get_icon("document-edit")

    def __init__(self, **kwargs):
        super(EditSettingsWidget, self).__init__(nodeName = "edit", **kwargs)
        self.setupUi(self)

    def loadSettings(self):
        super(EditSettingsWidget, self).loadSettings()

        self.spinBoxTabWidth.setValue(self.settings.value("tabWidth"))
        self.spinBoxIndentationWidth.setValue(self.settings.value("indentationWidth"))
        self.spinBoxWordLengthToComplete.setValue(self.settings.value("wordLengthToComplete"))

        self.checkBoxRemoveTrailingSpaces.setChecked(self.settings.value("removeTrailingSpaces"))
        self.checkBoxAutoBrackets.setChecked(self.settings.value("autoBrackets"))
        self.checkBoxSmartHomeSmartEnd.setChecked(self.settings.value("smartHomeSmartEnd"))
        self.checkBoxEnableAutoCompletion.setChecked(self.settings.value("enableAutoCompletion"))
        self.checkBoxAdjustIndentationOnPaste.setChecked(self.settings.value("adjustIndentationOnPaste"))
        self.radioButtonSpaces.setChecked(self.settings.value("indentUsingSpaces"))
        self.radioButtonTabulators.setChecked(not self.settings.value("indentUsingSpaces"))

    @QtCore.Slot(bool)
    def on_checkBoxRemoveTrailingSpaces_clicked(self, checked):
        self.settings.setValue('removeTrailingSpaces', self.checkBoxRemoveTrailingSpaces.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxAutoBrackets_clicked(self, checked):
        self.settings.setValue('autoBrackets', self.checkBoxAutoBrackets.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxSmartHomeSmartEnd_clicked(self, checked):
        self.settings.setValue('smartHomeSmartEnd', self.checkBoxSmartHomeSmartEnd.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxEnableAutoCompletion_clicked(self, checked):
        self.settings.setValue('enableAutoCompletion', self.checkBoxEnableAutoCompletion.isChecked())

    @QtCore.Slot(bool)
    def on_radioButtonSpaces_clicked(self, checked):
        self.settings.setValue('indentUsingSpaces', checked)

    @QtCore.Slot(bool)
    def on_checkBoxAdjustIndentationOnPaste_clicked(self, checked):
        self.settings.setValue('adjustIndentationOnPaste', self.checkBoxAdjustIndentationOnPaste.isChecked())

    @QtCore.Slot(int)
    def on_spinBoxTabWidth_valueChanged(self, value):
        self.settings.setValue('tabWidth', value)

    @QtCore.Slot(int)
    def on_spinBoxIndentationWidth_valueChanged(self, value):
        self.settings.setValue('indentationWidth', value)

    @QtCore.Slot(int)
    def on_spinBoxWordLengthToComplete_valueChanged(self, value):
        self.settings.setValue('wordLengthToComplete', value)
