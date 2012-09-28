#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui

from prymatex.core.plugin.dialog import PMXBaseDialog

from RequestItem.ui_requestitem import Ui_RequestItemDialog

class RequestItemDialog(QtGui.QDialog, Ui_RequestItemDialog, PMXBaseDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)

    def setParameters(self, parameters):
        if 'title' in parameters:
            self.setWindowTitle(parameters['title'])
        if 'prompt' in parameters:
            self.labelPrompt.setText(parameters['prompt'])
        if 'items' in parameters:
            for item in parameters['items']:
                self.comboBoxItems.addItem(item, item)
        if 'button1' in parameters:
            self.pushButton1.setText(parameters['button1'])
        if 'button2' in parameters:
            self.pushButton2.setText(parameters['button2'])
    
    def on_pushButton1_pressed(self):
        self.accept()
    
    def on_pushButton2_pressed(self):
        self.close()
        
    def execModal(self):
        code = self.exec_()
        if code == QtGui.QDialog.Accepted:
            return {'returnArgument': [self.comboBoxItems.itemData(self.comboBoxItems.currentIndex())]}
        return {}
        
dialogClass = RequestItemDialog
