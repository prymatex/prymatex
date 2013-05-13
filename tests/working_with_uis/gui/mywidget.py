from .ui_mywidget import Ui_MyWidget
from PyQt4.Qt import *

class MyWidget(QWidget, Ui_MyWidget):
    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self) # Importante!!
        
