#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex.core.plugin.dialog import PMXBaseDialog

from CommitDialog.ui_commit import Ui_CommitDialog

class CommitDialog(QtGui.QDialog, Ui_CommitDialog, PMXBaseDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        
    def setParameters(self, parameters):
        if "title" in parameters:
            self.setWindowTitle(parameters["title"])
        print parameters
    
    def execModal(self):
        code = self.exec_()
        if code == QtGui.QDialog.Accepted:
            return ""
        return 'dylan "este es el mensaje" archivo1 archivo2'
        
dialogClass = CommitDialog