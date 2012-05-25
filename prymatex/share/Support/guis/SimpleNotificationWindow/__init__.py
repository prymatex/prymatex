#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui

from prymatex.core.plugin.dialog import PMXBaseDialog

from SimpleNotificationWindow.ui_notification import Ui_NotificationDialog

class NotificationDialog(QtGui.QDialog, Ui_NotificationDialog, PMXBaseDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi(self)
        self.textEditSummary.setReadOnly(True)
        
    def setParameters(self, parameters):
        self.setWindowTitle(parameters["title"])
        self.labelLog.setText(parameters["log"])
        self.textEditSummary.setPlainText(parameters["summary"])
        
dialogClass = NotificationDialog