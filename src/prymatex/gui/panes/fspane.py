from PyQt4.QtGui import *
from PyQt4.QtCore import *

from prymatex.lib.i18n import ugettext as _
from prymatex.gui.utils import createButton
#from pr



class FSPaneWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupGui()
        self.tree.setRootIndex(self.tree.model().index(QDir.currentPath()))
        
    def setupGui(self):
        mainlayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        # Oneliner Watchout!! Sorry
        button_layout.addWidget(createButton(self, _("&Up")))
        button_layout.addWidget(createButton(self, _("&Filter")))
        button_layout.addStretch()
        mainlayout.addLayout(button_layout)
        self.tree = FSTree(self)
        mainlayout.addWidget(self.tree)
        self.setLayout(mainlayout)
    

class FSTree(QTreeView):
    def __init__(self, parent):
        QTreeView.__init__(self, parent)
        model = QDirModel(self)
        self.setModel(model)
        self.setAnimated(False)
        self.setIndentation(20)
        self.setSortingEnabled(True)
        
    def mouseDoubleClickEvent(self, event):
        index = self.indexAt(event.pos())
        print self.model().data(index).toPyObject()
        print self.model().data(index.parent()).toPyObject()
        print self.rootIndex()
    


class FSPane(QDockWidget):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("File System Panel"))
        self.setWidget(FSPaneWidget(self))
        
        