from PyQt4.QtGui import *
from PyQt4.QtCore import *
from prymatex.gui.panes import PaneDockBase
from prymatex.gui import PMXBaseGUIMixin
import shutil
import os
from os.path import abspath, join, dirname, isdir, isfile, basename
from prymatex.lib.i18n import ugettext as _
from prymatex.gui.utils import createButton, addActionsToMenu
from prymatex.gui.panes.ui_browser import Ui_Browser

class BrowserPaneWidget(QWidget, Ui_Browser, PMXBaseGUIMixin):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setObjectName('BrowserPaneWidget')
        self.setupUi(self)

    def setHtml(self, string):
        self.view.setHtml(string)
        
class PMXBrowserPaneDock(PaneDockBase):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Browser Panel"))
        self.setWidget(BrowserPaneWidget(self))

    def setHtml(self, string):
        self.widget().setHtml(string)

