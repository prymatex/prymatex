#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from PyQt4 import QtGui
from prymatex.ui.emergencytrace import Ui_TracebackDialog

class PMXTraceBackDialog(QtGui.QDialog, Ui_TracebackDialog):
    '''
    Crash dialog, shown when a fatal exception occurs
    '''
    def __init__(self, exception, explanation = None):
        '''
        @param exception: An exceptino instance
        @param explanation: Some explanation about what has happened
        '''
        assert isinstance(exception, Exception)
        if not explanation:
            explanation = self.trUtf8("An exception has occured")
        self.setWindowTitle("%s" % type(exception).__name__)
        self.textStackTrace.setPlainText(traceback.format_exc())
        
    def on_pushCopy_pressed(self):
        '''
        Copies text to the clipboard
        '''
        text = self.textStackTrace.toPlainText()
        QtGui.qApp.instance().clipboard().setText(text)
        
        