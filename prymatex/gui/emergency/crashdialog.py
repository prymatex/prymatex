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
        text = unicode(traceback_text)
        self.textEdit.setText(self.format(traceback_text))
        if show_through_stderr:
            sys.stderr.write(text)
            sys.stderr.flush()
            
    def format(self, some_code):
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
        