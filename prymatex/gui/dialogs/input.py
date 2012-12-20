#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.qt import QtGui

class ReplaceRenameInputDialog(QtGui.QInputDialog):
    Cancel = QtGui.QMessageBox.Cancel
    Rename = QtGui.QMessageBox.Ok
    Replace = QtGui.QMessageBox.Discard
    
    def showEvent(self, event):
        self.buttons = self.layout().itemAt(2).widget()
        self.buttons.button(QtGui.QDialogButtonBox.Ok).setText("Rename")
        self.replaceButton = self.buttons.addButton("Replace", QtGui.QDialogButtonBox.DestructiveRole)
        self.replaceButton.pressed.connect(self.on_replaceButton_pressed)
        QtGui.QInputDialog.showEvent(self, event)

    def on_replaceButton_pressed(self):
        self.done(QtGui.QDialogButtonBox.DestructiveRole)
        
    @classmethod
    def getText(cls, parent, title, label, mode = QtGui.QLineEdit.Normal, text = ""):
        inputDialog = cls(parent)
        inputDialog.setTextValue(text)
        inputDialog.setWindowTitle(title)
        inputDialog.setLabelText(label)
        if inputDialog.exec_():
            return inputDialog.textValue(), QtGui.QDialogButtonBox.DestructiveRole == inputDialog.result() and ReplaceRenameInputDialog.Replace or ReplaceRenameInputDialog.Rename
        return inputDialog.textValue(), ReplaceRenameInputDialog.Cancel
