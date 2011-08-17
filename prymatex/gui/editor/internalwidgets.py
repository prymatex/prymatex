'''
Some custom widgets used in the editor widget class
'''

from PyQt4.QtGui import QComboBox, QSpinBox, QWidget, QTextCursor, QTextDocument
from PyQt4.QtCore import Qt, pyqtSignal, QRegExp
from prymatex.core.base import PMXObject


class PMXRefocusWidget(QWidget, PMXObject):
    '''
    Refoucs Editor when the widget is hidden
    '''
    showed = pyqtSignal()
       
    def hideEvent(self, event):
        super(PMXRefocusWidget, self).hideEvent(event)
        self.mainWindow.currentEditorWidget.setFocus(Qt.MouseFocusReason)
        
    def showEvent(self, event):
        super(PMXRefocusWidget, self).showEvent(event)
        self.showed.emit()


        


class PMXSpinGoToLine(QSpinBox):
    editionFinished = pyqtSignal()
    KEY_TRIGGERS = (Qt.Key_Escape, )
    
    def __init__(self, parent = None):
        super(PMXSpinGoToLine, self).__init__(parent)
        self.setMinimum(1) # There's no line 0
    
    def showEvent(self, event):
        super(PMXSpinGoToLine, self).showEvent(event)
        self.selectAll()    # Select all text
        
    def keyPressEvent(self, event):
        super(PMXSpinGoToLine, self).keyPressEvent(event)
        if event.key() in self.KEY_TRIGGERS:
            self.editionFinished.emit()