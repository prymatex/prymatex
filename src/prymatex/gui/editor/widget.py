'''
'''
from PyQt4.QtGui import QWidget, QAction, QMenu, QKeySequence
from PyQt4.QtGui import QFont, QMessageBox
from PyQt4.QtCore import SIGNAL, Qt
from logging import getLogger
import sys
import traceback
import re
import logging

logger = logging.getLogger(__name__)

#PMX Libs
if __name__ == "__main__":
    from os.path import *
    pmx_base = abspath(join(dirname(__file__), '..', '..', '..'))
    sys.path.append(pmx_base)
    sys.path.append('../..')
    #pmx_base = abspath(join(dirname(__file__), '..', '..', '..'))
else:
    pass


from ui_editorwidget import Ui_EditorWidget

_counter = 0

def untitled_cunter():
    '''
    Genreates a sequence of numbers for the untitled documents
    Each call produces an incremental number
    '''
    global _counter
    tmp =  _counter
    _counter += 1
    return tmp
    

class PMXEditorWidget(QWidget, Ui_EditorWidget):
    
    def __init__(self, parent):
        super(PMXEditorWidget, self).__init__(parent)
        self.setupActions()
        self.setupUi(self)
        #self.connectActionToGui()
        self.setupFindReplaceWidget()
        #self.findreplaceWidget.hide()
        self.codeEdit.setFont(QFont("Monospace", 12))

        self.codeEdit.addAction(self.actionFind)
        self.codeEdit.addAction(self.actionReplace)

        self.findreplaceWidget.hide()

    @classmethod
    def getEditor(cls, parent,  path = None):
        '''
        Factory for the default text editor
        '''
        assert isinstance(parent, QWidget), self.trUtf8("You didn't pass a valid parent: %s" % parnet)
        return PMXEditorWidget(parent)

    @classmethod
    def registerEditor(cls, editor_cls):
        '''
        Register an edior class.
        
        '''
        pass


    
    @property
    def title(self):
        doc_title = unicode(self.trUtf8("Untitled %d"))
        return  doc_title % untitled_cunter()

    def setupActions(self):
        # Search
        self.actionFind = QAction("&Find", self)
        self.actionFind.setObjectName("actionFind")
        self.actionFind.setShortcut(QKeySequence(self.trUtf8("Ctrl+F")))
        # Replace
        self.actionReplace = QAction(self.trUtf8("Find and &Replce"), self)
        self.actionReplace.setObjectName("actionReplace")
        self.actionReplace.setShortcut(QKeySequence(self.trUtf8("Ctrl+R")))



    
    def on_actionFind_triggered(self):
        self.hideReplaceWidgets()
        self.findreplaceWidget.show()
        self.comboFind.setFocus(Qt.MouseFocusReason)


    def on_actionReplace_triggered(self):
        self.showReplaceWidgets()
        self.findreplaceWidget.show()
        self.comboFind.setFocus(Qt.MouseFocusReason)
        


    #TODO: @diego Too complex? Would it be better to make it more explicit?
    @property
    def replaceWidgets(self):
        return map(lambda name: getattr(self, name), ("labelReplaceWith", "comboReplace",
                                                      "pushReplaceAndFindPrevious",
                                                      "pushReplaceAndFindNext",
                                                      "pushReplaceAll"))
    def hideReplaceWidgets(self):
        map(lambda w: w.hide(), self.replaceWidgets)

    def showReplaceWidgets(self):
        map(lambda w: w.show(), self.replaceWidgets)

        
    def setupFindReplaceWidget(self):
        self.actionRegex = QAction(self.trUtf8("Use &regular expressions"),self)
        self.actionRegex.setCheckable(True)
        
        self.actionWholeWord = QAction(self.trUtf8("Find &whole word only"), self)
        self.actionWholeWord.setCheckable(True)

        self.actionCaseSensitive = QAction(self.trUtf8("Case &Sensitive"), self)
        self.actionCaseSensitive.setCheckable(True)

        self.menuOptions = QMenu()
        self.menuOptions.addAction(self.actionRegex)
        self.menuOptions.addAction(self.actionWholeWord)
        self.menuOptions.addAction(self.actionCaseSensitive)

        self.pushOptions.setMenu(self.menuOptions)

    def on_pushCloseFindreplace_pressed(self):
        self.findreplaceWidget.hide()

    def requestClose(self, *largs):
        
        if self.codeEdit.document().isModified():
            QMessageBox.information(self, "", "AA")
        else:
            return True
        
        
if __name__ == "__main__":
    from PyQt4.QtGui import QApplication, QFont, QWidget, QVBoxLayout
    from PyQt4.QtGui import QPushButton
    app = QApplication(sys.argv)
    app.logger = {}
    win = PMXEditorWidget(None) # No Parent
    win.show()
    sys.exit(app.exec_())