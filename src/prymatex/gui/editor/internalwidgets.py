'''
Some custom widgets used in the editor widget class
'''

from PyQt4.QtGui import QComboBox, QSpinBox, QWidget
from PyQt4.QtCore import Qt, pyqtSignal
from prymatex.core.base import PMXObject


class PMXRefocusWidget(QWidget, PMXObject):
    '''
    Refoucs Editor when the widget is hidden
    '''
    showed = pyqtSignal()
       
    def hideEvent(self, event):
        super(PMXRefocusWidget, self).hideEvent(event)
        self.mainwindow.currentEditorWidget.setFocus(Qt.MouseFocusReason)
        
    def showEvent(self, event):
        super(PMXRefocusWidget, self).showEvent(event)
        self.showed.emit()
        
        
class PMXFindBox(QComboBox):
    editionFinished = pyqtSignal()
    KEY_TRIGGERS = (Qt.Key_Escape, )
    def keyPressEvent(self, event):
        super(PMXFindBox, self).keyPressEvent(event)
        if event.key() in self.KEY_TRIGGERS:
            self.editionFinished.emit()

class PMXReplaceBox(QComboBox):
    editionFinished = pyqtSignal()
    KEY_TRIGGERS = (Qt.Key_Escape, )
    def keyPressEvent(self, event):
        super(PMXReplaceBox, self).keyPressEvent(event)
        if event.key() in self.KEY_TRIGGERS:
            self.editionFinished.emit()


class PMXCommonSearchBox(QComboBox):
    '''
    Common behaviour between the search and replace widgtets
    '''
    editionFinished = pyqtSignal()
    KEY_TRIGGERS = (Qt.Key_Escape, )
    
    def keyPressEvent(self, event):
        super(PMXCommonSearchBox, self).keyPressEvent(event)
        if event.key() in self.KEY_TRIGGERS:
            self.editionFinished.emit()
        


class PMXSpinGoToLine(QSpinBox):
    editionFinished = pyqtSignal()
    KEY_TRIGGERS = (Qt.Key_Escape, )
    
    def __init__(self, parent = None):
        super(PMXSpinGoToLine, self).__init__(parent)
        self.setMinimum(1) # There's no line 0
        
    def keyPressEvent(self, event):
        super(PMXSpinGoToLine, self).keyPressEvent(event)
        if event.key() in self.KEY_TRIGGERS:
            self.editionFinished.emit()