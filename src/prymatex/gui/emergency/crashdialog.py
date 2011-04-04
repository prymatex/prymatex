from PyQt4.Qt import *

from ui_crash import Ui_CrashDialog


class PMXCrashDialog(QDialog, Ui_CrashDialog):
    '''
        Emergency Dialog
    '''
    def __init__(self, traceback_text):
        super(PMXCrashDialog, self).__init__()
        self.setupUi(self)
        self.textEdit.setText(unicode(traceback_text))
    
    def on_pushCopyTraceback_pressed(self):
        clipboard = qApp.instance().clipboard()
        clipboard.setText(self.textEdit.toPlainText())
        