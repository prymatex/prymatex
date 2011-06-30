
from ui_trace import Ui_TracebackDialog
from PyQt4.QtGui import QDialog, qApp
import traceback

class PMXTraceBackDialog(QDialog, Ui_TracebackDialog):
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
        qApp.instance().clipboard().setText(text)
        
        