# coding: utf-8

from PyQt4.QtGui import QWidget

class PMXBaseGUIMixin(object):
    '''
    Define some shorcut properties to current editor
    and current panes.
    '''
    
    _mainWindow = None
    _currentEditor = None
    
    def _getMainWindow(self):
        if not isinstance(self, QWidget):
            raise Exception("%s can be used only on QWidgets" % 
                            self.__class__.__name__)
        if self._mainWindow is None:
            c = self
            while c.__class__.__name__ != 'PMXMainWindow':
                c = c.parent()
            if c is None:
                raise Exception("Could not find parent main window from %s" %
                                self)
            self._mainWindow = c
        return self._mainWindow
       
    mainwindow = property(_getMainWindow)
    
    def getCurrentEditor(self): 
        return self.mainWindow.tabWidgetEditors.currentWidget()
       
    currentEditor = property(getCurrentEditor)