# -*- coding: utf-8 -*-
import sys
import os
#from prymatex.gui.widgets.overlay import PMXMessageOverlay
from imp import PMXMessageOverlay
sys.path.append(os.path.abspath('..'))

import re
from PyQt4 import QtCore, QtGui

class ExampleOverlayedText(QtGui.QPlainTextEdit, PMXMessageOverlay):
    
    FULL_THERESHOLD = 0.4
    
    def __init__(self, parent = None):
        QtGui.QTextEdit.__init__(self, parent)
        PMXMessageOverlay.__init__(self)
        self.blockCountChanged.connect(self.showBlockCount)
        self.selectionChanged.connect(self.showRandomMessage)
        
    def showRandomMessage(self):
        x, y = random.randint(0, self.width() - self.messageOverlay.width()), random.randint(0, self.height() - self.messageOverlay.width())
        self.showMessage("Selection changed", pos = (x, y))
              
    def resizeEvent(self, event):
        super(ExampleOverlayedText, self).resizeEvent(event)
        self.updateMessagePosition()
        
    def messageLinkActivated(self, link):
        QtGui.QMessageBox.information(self, "Link activated", "You just clicked on %s" % link)

    def showBlockCount(self, newCount):
        text = "<a href='coquitos'>Copy</a> Block count changed to <i><b>%s</b></i>" % newCount
        self.showMessage(text,
                         hrefCallbacks={'coquitos': lambda s=text: QtGui.qApp.instance().setClipboard(s)})
    
import random
random.seed(os.getpid())
if __name__ == "__main__":
    from pygments_stuff import Highlighter
    app = QtGui.QApplication(sys.argv)
    
#    rst = ExampleOverlayedText()
#    rst.setWindowTitle('reSt')
#    hl=Highlighter(rst.document(),"rest")
#    rst.show()

    python = ExampleOverlayedText()
    python.setWindowTitle('python')
    hl=Highlighter(python.document(),"python")
    python.show()

    sys.exit(app.exec_())