#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.Qt import *
from prymatex.ui.emergencycrash import Ui_CrashDialog
import sys

class PMXCrashDialog(QDialog, Ui_CrashDialog):
    '''
    Show a nice traceback dialog
    '''
    #TODO: Impement send to in the crash dialog button
    def __init__(self, traceback_text, show_through_stderr = True):
        super(PMXCrashDialog, self).__init__()
        self.setupUi(self)
        self.pushSendTraceback.setEnabled(True) #Testing
        self.fillTracebackTextEdit(traceback_text)
        if show_through_stderr:
            sys.stderr.write(traceback_text)
            sys.stderr.flush()
        
    def fillTracebackTextEdit(self, content):
        text = content#.decode('utf-8')
        self.textEdit.setText(self.format(text))
            
    def format(self, some_code):
        ''' If pygment's available it will highlight the
        traceback with HTML, allowing Qt's integrated text
        browser to display it nicely :) '''
        try:
            from pygments import highlight
            from pygments.lexers import PythonLexer
            from pygments.formatters import HtmlFormatter
            return highlight(some_code, PythonLexer(), HtmlFormatter(noclasses = True))
        except ImportError:
            return some_code
    
    def on_pushCopyTraceback_pressed(self):
        clipboard = qApp.instance().clipboard()
        clipboard.setText(self.textEdit.toPlainText())
    
    def on_pushSendTraceback_pressed(self):
        res = QMessageBox.information(self, "Send traceback", "Send current traceback to "
                                "Prymatex deevelopers?")
        print res