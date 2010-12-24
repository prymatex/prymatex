'''
'''
from PyQt4.QtGui import QWidget, QAction, QMenu, QKeySequence
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


class PMXEditorWidget(QWidget, Ui_EditorWidget):
    def __init__(self, parent):
        super(PMXEditorWidget, self).__init__(parent)
        self.setupUi(self)
        self.setupFindReplaceWidget()
        #self.findreplaceWidget.hide()
        self.codeEdit.setFont(QFont("Monospace", 12))

        # Test
        if not parent:
            print "Creando QAction del find"
            self.actionFind = QAction("find", self)
            self.codeEdit.addAction(self.actionFind)
            self.actionFind.setShortcut(QKeySequence("Ctrl+F"))
            self.connect(self.actionFind, SIGNAL("triggered()"), self.openFindreplaceWidget) # Test


    def setupAction(self):
        pass

    
    def openFindreplaceWidget(self):
        self.findreplaceWidget.show()
        self.comboFind.setFocus(Qt.MouseFocusReason)
    
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
        
if __name__ == "__main__":
    from PyQt4.QtGui import QApplication, QFont, QWidget, QVBoxLayout
    from PyQt4.QtGui import QPushButton
    app = QApplication(sys.argv)
    app.logger = {}
    win = PMXEditorWidget(None) # No Parent
    win.show()
    sys.exit(app.exec_())