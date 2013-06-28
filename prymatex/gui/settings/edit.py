#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore
from prymatex import resources

from prymatex.ui.configure.edit import Ui_Edit
from prymatex.models.settings import SettingsTreeNode

class EditSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_Edit):
    NAMESPACE = "editor"
    TITLE = "Edit"
    ICON = resources.getIcon("document-edit")

    def __init__(self, settingGroup, profile = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "edit", settingGroup, profile)
        self.setupUi(self)

    def loadSettings(self):
        SettingsTreeNode.loadSettings(self)
        
        self.spinBoxTabWidth.setValue(self.settingGroup.value("tabWidth"))
        self.spinBoxIndentationWidth.setValue(self.settingGroup.value("indentationWidth"))
        self.spinBoxWordLengthToComplete.setValue(self.settingGroup.value("wordLengthToComplete"))
        
        self.checkBoxRemoveTrailingSpaces.setChecked(self.settingGroup.value("removeTrailingSpaces"))
        self.checkBoxAutoBrackets.setChecked(self.settingGroup.value("autoBrackets"))
        self.checkBoxSmartHomeSmartEnd.setChecked(self.settingGroup.value("smartHomeSmartEnd"))
        self.checkBoxEnableAutoCompletion.setChecked(self.settingGroup.value("enableAutoCompletion"))
        self.checkBoxAdjustIndentationOnPaste.setChecked(self.settingGroup.value("adjustIndentationOnPaste"))
        self.radioButtonSpaces.setChecked(self.settingGroup.value("tabStopSoft"))
        self.radioButtonTabulators.setChecked(not self.settingGroup.value("tabStopSoft"))
        
    def on_checkBoxRemoveTrailingSpaces_toggled(self, checked):
        self.settingGroup.setValue('removeTrailingSpaces', self.checkBoxRemoveTrailingSpaces.isChecked())
    
    def on_checkBoxAutoBrackets_toggled(self, checked):
        self.settingGroup.setValue('autoBrackets', self.checkBoxAutoBrackets.isChecked())
    
    def on_checkBoxSmartHomeSmartEnd_toggled(self, checked):
        self.settingGroup.setValue('smartHomeSmartEnd', self.checkBoxSmartHomeSmartEnd.isChecked())
    
    def on_checkBoxEnableAutoCompletion_toggled(self, checked):
        self.settingGroup.setValue('enableAutoCompletion', self.checkBoxEnableAutoCompletion.isChecked())

    def on_radioButtonSpaces_toggled(self, checked):
        self.settingGroup.setValue('tabStopSoft', checked)
    
    def on_checkBoxAdjustIndentationOnPaste_toggled(self, checked):
        self.settingGroup.setValue('adjustIndentationOnPaste', self.checkBoxAdjustIndentationOnPaste.isChecked())
        
    @QtCore.Slot(int)
    def on_spinBoxTabWidth_valueChanged(self, value):
        self.settingGroup.setValue('tabWidth', value)
    
    @QtCore.Slot(int)
    def on_spinBoxIndentationWidth_valueChanged(self, value):
        self.settingGroup.setValue('indentationWidth', value)

    @QtCore.Slot(int)
    def on_spinBoxWordLengthToComplete_valueChanged(self, value):
        self.settingGroup.setValue('wordLengthToComplete', value)
