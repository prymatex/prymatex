# Layout manager
'''

'''
from PyQt4.Qt import *
from logging import getLogger

from tabwidget import PMXTabWidget

logger = getLogger(__file__)

class PMXLayoutManager(QWidget):

    def __init__(self, parent):
        super(PMXLayoutManager, self).__init__(parent)
        self.setObjectName("PMXLayoutManager")
        
        self.setLayout(self.getDefaultLayout())

        self.layout().addWidget(PMXTabWidget(self))
        self.layout().addWidget(PMXTabWidget(self))
        
        #self.layout().addWidget(QTextEdit())
        #self.setLayout(layout)
        #layout.addWidget(QLineEdit())
        
        #logger.debug("Creando el layout manager")
        # Reload config?

    def getDefaultLayout(self):
        return QVBoxLayout()
        

    def setLayout(self, layout):
        if not layout:
            pass
        QWidget.setLayout(self, layout)
    def splitVertical(self):
        pass

    def splitHorizontal(self):
        pass

    @property
    def currentTabWidget(self):
        pass

    def addNewTab(self):
        pass
    
        


