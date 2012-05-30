#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex.core.plugin.dialog import PMXBaseDialog

from ProgressDialog.ui_progress import Ui_ProgressDialog

# {   'title': 'Progress', 
#     'summary': u'Creating HTML version of document\u2026', 
#     'details': '', 
#     'isIndeterminate': True, 
#     'progressAnimate': True
# }

class ProgressDialog(QtGui.QDialog, Ui_ProgressDialog, PMXBaseDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        self.progressAnimate = False
        self.animateTimer = QtCore.QTimer(self)
        self.animateTimer.timeout.connect(self.updateProgressValue)
        self.currentProgressValue = 0
        self.milestoneProgressValue = 0
        
    def updateProgressValue(self):
        self.currentProgressValue += 1
        if self.currentProgressValue <= self.milestoneProgressValue:
            self.progressBar.setValue(self.currentProgressValue)
        else:
            self.animateTimer.stop()
        
    def setParameters(self, parameters):
        if "title" in parameters:
            self.setWindowTitle(parameters["title"])
        if "progressAnimate" in parameters:
            self.progressAnimate = parameters["progressAnimate"]
        if "isIndeterminate" in parameters and parameters["isIndeterminate"]:
            self.progressBar.setMaximum(0)
        if "details" in parameters:
            print parameters["details"]
        if "summary" in parameters:
            print parameters["summary"]
        if "progressValue" in parameters and self.progressAnimate:
            self.milestoneProgressValue = parameters["progressValue"]
            self.animateTimer.start(10)
        elif "progressValue" in parameters:
            self.progressBar.setValue(parameters["progressValue"])
        
dialogClass = ProgressDialog