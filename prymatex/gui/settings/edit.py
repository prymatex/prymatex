#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.ui.configure.edit import Ui_Edit
from prymatex.models.settings import SettingsTreeNode

class EditSettingsWidget(SettingsTreeNode, Ui_Edit, QtWidgets.QWidget):
    NAMESPACE = "editor"

    def __init__(self, component_class, **kwargs):
        super(EditSettingsWidget, self).__init__(component_class, nodeName="edit", **kwargs)
        self.setupUi(self)
        
    def loadSettings(self):
        super(EditSettingsWidget, self).loadSettings()
        self.setTitle("Edit")
        self.setIcon(self.application().resources().get_icon("settings-edit"))

        self.spinBoxIndentationWidth.setValue(self.settings().get("indentation_width"))
        self.spinBoxWordLengthToComplete.setValue(self.settings().get("word_length_to_complete"))

        self.checkBoxRemoveTrailingSpaces.setChecked(self.settings().get("remove_trailing_spaces"))
        self.checkBoxAutoBrackets.setChecked(self.settings().get("auto_brackets"))
        self.checkBoxSmartHomeSmartEnd.setChecked(self.settings().get("smart_home_smart_end"))
        self.checkBoxEnableAutoCompletion.setChecked(self.settings().get("enable_auto_completion"))
        self.checkBoxAdjustIndentationOnPaste.setChecked(self.settings().get("adjust_indentation_on_paste"))
        self.radioButtonSpaces.setChecked(self.settings().get("indent_using_spaces"))
        self.radioButtonTabulators.setChecked(not self.settings().get("indent_using_spaces"))

    @QtCore.Slot(bool)
    def on_checkBoxRemoveTrailingSpaces_clicked(self, checked):
        self.settings().set('remove_trailing_spaces', self.checkBoxRemoveTrailingSpaces.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxAutoBrackets_clicked(self, checked):
        self.settings().set('auto_brackets', self.checkBoxAutoBrackets.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxSmartHomeSmartEnd_clicked(self, checked):
        self.settings().set('smart_home_smart_end', self.checkBoxSmartHomeSmartEnd.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxEnableAutoCompletion_clicked(self, checked):
        self.settings().set('enable_auto_completion', self.checkBoxEnableAutoCompletion.isChecked())

    @QtCore.Slot(bool)
    def on_radioButtonSpaces_clicked(self, checked):
        self.settings().set('indent_using_spaces', checked)

    @QtCore.Slot(bool)
    def on_checkBoxAdjustIndentationOnPaste_clicked(self, checked):
        self.settings().set('adjust_indentation_on_paste', self.checkBoxAdjustIndentationOnPaste.isChecked())

    @QtCore.Slot(int)
    def on_spinBoxIndentationWidth_valueChanged(self, value):
        self.settings().set('indentation_width', value)

    @QtCore.Slot(int)
    def on_spinBoxWordLengthToComplete_valueChanged(self, value):
        self.settings().set('word_length_to_complete', value)

