from PyQt4.Qt import *
from ui_crash import Ui_CrashDialog
import sys

class PMXCrashDialog(QDialog, Ui_CrashDialog):
    '''
        Emergency Dialog
    '''
    
    def __init__(self, traceback_text, show_through_stderr = True):
        super(PMXCrashDialog, self).__init__()
        self.setupUi(self)
        text = unicode(traceback_text)
        self.textEdit.setText(text)
        if show_through_stderr:
            sys.stderr.write(text)
            sys.stderr.flush()
    
    def on_pushCopyTraceback_pressed(self):
        clipboard = qApp.instance().clipboard()
        clipboard.setText(self.textEdit.toPlainText())
        