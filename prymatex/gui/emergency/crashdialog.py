#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore

from prymatex.ui.emergencycrash import Ui_CrashDialog
from prymatex.gui.emergency.beautify import beautifyTraceback

class PMXCrashDialog(QtCore.QDialog, Ui_CrashDialog):
    """
    Show a nice traceback dialog
    """
    
    def __init__(self, tracebackText, show_through_stderr = True):
        QtCore.QDialog.__init__(self)
        self.setupUi(self)
        self.pushSendTraceback.setEnabled(True) #Testing
        self.textEdit.setText(beautifyTraceback(tracebackText))
        if show_through_stderr:
            sys.stderr.write(tracebackText)
            sys.stderr.flush()
    
    def on_pushCopyTraceback_pressed(self):
        clipboard = qApp.instance().clipboard()
        clipboard.setText(self.textEdit.toPlainText())
    
    def on_pushSendTraceback_pressed(self):
        res = QMessageBox.information(self, "Send traceback", "Send current traceback to "
                                "Prymatex deevelopers?")
        print(res)
        
    def on_pushClose_pressed(self):
        self.accept()