from PyQt4.QtGui import QTreeView
from PyQt4.QtCore import pyqtSignal, pyqtSignature
class PMXConfigTreeView(QTreeView):
    _model = None
    
    widgetChanged = pyqtSignal(int)
    
    def __init__(self, parent = None):
        super(PMXConfigTreeView, self).__init__(parent)
        
    
    
    
    def currentChanged(self, new, old):
        model = self.model()
        new, old = map( lambda indx: model.itemFromIndex(indx), (new, old))
        print new, old, map(type, [old, new])
        self.widgetChanged.emit(new.widget_index)
        
        
    