from PyQt4.QtGui import QApplication, QDialog, qApp
import sys

from ui_dialog import Ui_CrashDialog
from traceback import format_exc
 
class PMXExceptionExplantaionDialog(QDialog, Ui_CrashDialog):
    '''
        Emergency Dialog
    '''
    def __init__(self, traceback_text):
        super(PMXExceptionExplantaionDialog, self).__init__()
        self.setupUi(self)
        self.textEdit.setText(unicode(traceback_text))
    
    def on_pushCopyTraceback_pressed(self):
        clipboard = qApp.instance().clipboard()
        clipboard.setText(self.textEdit.toPlainText())