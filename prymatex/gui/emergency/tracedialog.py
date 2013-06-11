#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
from prymatex.qt import QtGui
from prymatex.ui.emergencytrace import Ui_TracebackDialog
from traceback import format_exception
from .beautify import beautifyTraceback

class PMXTraceBackDialog(QtGui.QDialog, Ui_TracebackDialog):
    '''
    Crash dialog, shown when a fatal exception occurs
    '''
    def __init__(self, parent = None):
        '''
        @param exception: An exceptino instance
        '''
        super(PMXTraceBackDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.connectSignals()
    
    def connectSignals(self):
        self.pushButtonKillApp.pressed.connect(QtGui.QApplication.quit)
        
    def on_pushCopy_pressed(self):
        '''
        Copies text to the clipboard
        '''
        text = self.textStackTrace.toPlainText()
        QtGui.qApp.instance().clipboard().setText(text)
    
    @classmethod
    def fromLastException(cls, exception, parent = None):
        '''
        Factory for exception
        '''
        assert isinstance(exception, Exception)
        inst = cls()
        inst.setWindowTitle("%s" % type(exception).__name__)
        inst.textStackTrace.setPlainText(traceback.format_exc())
        return inst
    
    @classmethod
    def fromSysExceptHook(cls, exctype, value, traceback, parent = None):
        ''' Creates a dialgo from sysexcepthook arguments,
        better suited for sys.excepthook handling '''
        inst = cls()
        inst.setWindowTitle("Unhandled Exception")
        tracebackText = ''.join(format_exception(type, value, traceback))
        inst.textStackTrace.setHtml(beautifyTraceback(tracebackText))
        return inst
    
    