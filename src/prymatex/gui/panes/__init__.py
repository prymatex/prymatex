from PyQt4.QtCore import SIGNAL

class ShowHideSignalsMixin(object):
    '''
    Provides some useful functions
    '''
    def showEvent(self, event):
        self.emitWidgetShown(False)
    
    def hideEvent(self, event):
        self.emitWidgetShown(True)
        
    def emitWidgetShown(self, val):
        print "self.emitWidgetShown(True)", val    
        self.emit(SIGNAL('widgetShown(bool)'), val)
    
    
    
    