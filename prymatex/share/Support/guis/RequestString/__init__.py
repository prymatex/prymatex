#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui

from prymatex.core.plugin.dialog import PMXBaseDialog

from RequestString.ui_requeststring import Ui_RequestStringDialog

class RequestStringDialog(QtGui.QDialog, Ui_RequestStringDialog, PMXBaseDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        
    def setParameters(self, parameters):
        if 'title' in parameters:
            self.setWindowTitle(parameters['title'])
        if 'prompt' in parameters:
            self.labelPrompt.setText(parameters['prompt'])
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
            return {'returnArgument': self.lineEdit.text()}
        return {}
        
dialogClass = RequestStringDialog