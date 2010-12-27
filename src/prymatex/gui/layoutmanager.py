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

        #TODO: Make this dynamic
        self.widget = PMXTabWidget(self)
        self.layout().addWidget( self.widget )
        #self.layout().addWidget(PMXTabWidget(self))
        


    def getDefaultLayout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        return layout
        
    
    
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
        #focused_widget = qApp.instance().focusWidget()
        return self.widget

    def addNewTab(self):
        pass
    
    def currentEditor(self):
        '''
        Returns the current editor
        '''
        self.currentTabWidget.currentWidget()