from PyQt4.Qt import *
from logging import getLogger

logger = getLogger(__file__)

class BaseProxy(QObject):
    '''
    Base proxy for 
    '''
    def __init__(self, parent):
        super(BaseProxy, self).__init__(parent)

    @property
    def widget(self):
        return self.parent()


class TabWidgetProxy(BaseProxy):
    '''
    Proxies current TabWidget
    '''
    
    def openFile(self, path):
        #self.widget.centralWidget()
        print "Proxy Open File", path
    


class CurrentEditorProxy(BaseProxy):
    '''
    Proxies current editor
    '''
    pass