from PyQt4.QtGui import QTreeView, QWidget

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
        


from ui_font_and_theme import Ui_FontThemeConfig 
class PMXThemeConfigWidget(QWidget, Ui_FontThemeConfig):
    def __init__(self, parent = None):
        super(PMXThemeConfigWidget, self).__init__(parent)
        self.setupUi(self)

from ui_updates import Ui_Updates
class PMXUpdatesWidget(QWidget, Ui_Updates):
    def __init__(self, parent = None):
        super(PMXUpdatesWidget, self).__init__(parent)
        self.setupUi(self)
        
from ui_general import Ui_General
class PMXGeneralWidget(QWidget, Ui_General):
    def __init__(self, parent = None):
        super(PMXGeneralWidget, self).__init__(parent)
        self.setupUi(self)
        
        
        