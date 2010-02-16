from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDockWidget

class PaneDockBase(QDockWidget):
    '''
    Provides some useful functions
    '''
    def showEvent(self, event):
        QDockWidget.showEvent(self, event)
        self.emitWidgetShown(True)
    
    def hideEvent(self, event):
        QDockWidget.hideEvent(self, event)
        self.emitWidgetShown(False)
        
    def emitWidgetShown(self, val):
        self.emit(SIGNAL('widgetShown(bool)'), val)
    
    
    
    