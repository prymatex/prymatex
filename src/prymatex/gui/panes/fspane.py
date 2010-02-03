from PyQt4.QtGui import *
from PyQt4.QtCore import *

from prymatex.lib.i18n import ugettext as _

class FSPane(QDockWidget):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("File System Panel"))
        

        self.model = QDirModel()
        self.tree = QTreeView(self)
        self.tree.setModel(self.model)

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.setWidget(self.tree)
        self.tree.setRootIndex(self.model.index(QDir.currentPath()))