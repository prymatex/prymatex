#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtWidgets

class ReplaceRenameInputDialog(QtWidgets.QInputDialog):
    Cancel = QtWidgets.QMessageBox.Cancel
    Rename = QtWidgets.QMessageBox.Ok
    Replace = QtWidgets.QMessageBox.Discard
    
    def showEvent(self, event):
        self.buttons = self.layout().itemAt(2).widget()
        self.buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Rename")
        self.replaceButton = self.buttons.addButton("Replace", QtWidgets.QDialogButtonBox.DestructiveRole)
        self.replaceButton.pressed.connect(self.on_replaceButton_pressed)
        super(ReplaceRenameInputDialog, self).showEvent(event)

    def on_replaceButton_pressed(self):
        self.done(QtWidgets.QDialogButtonBox.DestructiveRole)
        
    @classmethod
    def getText(cls, parent, title, label, mode = QtWidgets.QLineEdit.Normal, text = ""):
        inputDialog = cls(parent)
        inputDialog.setTextValue(text)
        inputDialog.setWindowTitle(title)
        inputDialog.setLabelText(label)
        if inputDialog.exec_():
            return inputDialog.textValue(), QtGui.QDialogButtonBox.DestructiveRole == inputDialog.result() and ReplaceRenameInputDialog.Replace or ReplaceRenameInputDialog.Rename
        return inputDialog.textValue(), ReplaceRenameInputDialog.Cancel
