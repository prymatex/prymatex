
from PyQt4.QtGui import QTabWidget, QTextEdit, QMessageBox
from PyQt4.QtCore import QString

from prymatex.lib.i18n import ugettext as _
import os

class PMXTextEdit(QTextEdit):
    
    def __init__(self, parent, path = None):
        QTextEdit.__init__(self, parent)
        if not path:
            return
        
        path = isinstance(path, QString) and unicode(path) or path
        if os.path.exists(path):
            try:
                f = open(path)
                text = f.read()
                f.close()
                self.setPlainText(text)
            except Exception, e:
                QMessageBox.critical(self, _("Read Error"), _("Could not read %s<br/>") % path)
            else:
                self.path = path
                
#    @property
#    def index(self):
#        tabwidget = self.parent()
#        for index in range(tabwidget.count()):
#            widget = tabwidget.widget(index)
#            print widget, self
#            if widget == self:
#                return index
#        return -1

    def setTitle(self, text):
        tabwidget = self.parent().parent()
        #print tabwidget, tabwidget.parent()
        index = tabwidget.indexOf(self)
        tabwidget.setTabText(index, text)
    
    def updateTitle(self):
        
        self.setTitle(os.path.basename(self.path))
        

class PMXTabWidget(QTabWidget):
    EDIT_TAB_WIDGET = PMXTextEdit
    UNTITLED_LABEL = _("New File") 
    
    
    def __init__(self, parent):
        QTabWidget.__init__(self, parent)
        if not self.count():
            self.appendEmptyTab()
        self.setTabsClosable(True)
        self.setMovable(True)
        
        #self.setTab
    
    
    def getEditor(self, *largs, **kwargs):
        '''
        Editor Factory
        '''
        return self.EDIT_TAB_WIDGET(self, *largs, **kwargs)
    
    def tabRemoved(self, index):
        if not self.count():
            self.appendEmptyTab()
    
    
    def openLocalFile(self, path):
        editor = self.getEditor(path)
        index = self.addTab(editor, _("Loading..."))
        self.setCurrentIndex(index)
        editor.updateTitle()
    
    
    def appendEmptyTab(self):
        editor = self.getEditor()
        index = self.addTab(editor, self.UNTITLED_LABEL)
        self.setCurrentIndex(index)