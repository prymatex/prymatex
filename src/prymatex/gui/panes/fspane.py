from PyQt4.QtGui import *

from prymatex.lib.i18n import ugettext as _

class FSPane(QDockWidget):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("File System Panel"))