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
        print parameters

    def execModal(self):
        code = self.exec_()
        if code == QtGui.QDialog.Accepted:
            return self.textValue()
        return ""
        
dialogClass = RequestStringDialog