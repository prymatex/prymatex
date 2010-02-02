from PyQt4.QtGui import QTabWidget, QTextEdit, QMessageBox
from prymatex.lib.i18n import ugettext as _
import os

class PMXTextEdit(QTextEdit):
    
    def __init__(self, parent, path = None):
        QTextEdit.__init__(self, parent)
        if os.path.exists(path):
            try:
                f = open(path)
                text = f.read()
                f.close()
                self.setPlainText(text)
            except Exception, e:
                QMessageBox.critical(self, _("Read Error"), _("Could not read %s<br/>") % path)
            else:
                name = os.path.basename(path)
                self.setTitle(name)
                

    def setTitle(self, text):
        tabwidget = self.parent()
        index = tabwidget.indexOf(self)
        tabwidget.setTabText(index, text)
        
        

class PMXTabWidget(QTabWidget):
    EDIT_TAB_WIDGET = PMXTextEdit
    UNTITLED_LABEL = _("New File") 
    
    
    def __init__(self, parent):
        QTabWidget.__init__(self, parent)
        if not self.count():
            self.appendEmptyTab()
    
    
    def getEditor(self):
        '''
        Editor Factory
        '''
        return self.EDIT_TAB_WIDGET(self)
    
    def tabRemoved(self, index):
        if not self.count():
            self.appendEmptyTab()
    
    
    def openLocalFile(self, path):
        #TODO: Make this work
        pass
    
    
    def appendEmptyTab(self):
        editor = self.getEditor()
        index = self.addTab(editor, self.UNTITLED_LABEL)
        self.setCurrentIndex(index)