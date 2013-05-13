#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtGui

from prymatex.core import PMXBaseDialog

from RequestSecureString.ui_requestsecurestring import Ui_RequestSecureStringDialog

class RequestSecureStringDialog(QtGui.QDialog, Ui_RequestSecureStringDialog, PMXBaseDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        
    def setParameters(self, parameters):
        print(parameters)
        
dialogClass = RequestSecureStringDialog