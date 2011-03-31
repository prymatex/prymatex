import os, shutil, logging
from os.path import abspath, join, dirname, isdir, isfile, basename
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from prymatex.gui.panes import PaneDockBase
from prymatex.gui import PMXBaseGUIMixin
from prymatex.lib.i18n import ugettext as _
from prymatex.gui.utils import createButton, addActionsToMenu
from prymatex.gui.panes.ui_fspane import Ui_FSPane
from prymatex.gui.panes.ui_fssettings import Ui_FSSettingsDialog
from prymatex.core.base import PMXObject
from prymatex.core.config import Setting

logger = logging.getLogger(__name__)

class FSPaneWidget(QWidget, Ui_FSPane, PMXBaseGUIMixin, PMXObject):
    filters = Setting(default = ['*~', '*.pyc'])
    
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setObjectName('FSPaneWidget')
        self.dialogConfigFilters = PMXFSPaneConfigDialog(self)
        self.setupUi(self)
        start_dir = qApp.instance().startDirectory()
        self.tree.setRootIndex(self.tree.model().index(start_dir))
        self.configure()
        
    class Meta:
        settings = "filemanager"
        
    @pyqtSignature('bool')
    def on_buttonSyncTabFile_toggled(self, sync):
        if sync:
            # Forzamos la sincronizacion
            editor = self.mainwindow.current_editor_widget
            self.tree.focusWidgetPath(editor)

    @pyqtSignature('')
    def on_buttonUp_pressed(self):
        #QMessageBox.information(self, "UP", "Up")
        #self.get
        self.tree.goUp()
    
    @pyqtSignature('')
    def on_buttonCollapseAll_pressed(self):
        self.tree.collapseAll()
        #self.buttonSyncTabFile.setEnabled(False)
    
    def on_buttonFilter_pressed(self):
        self.dialogConfigFilters.exec_()

class PMXFSPaneConfigDialog(Ui_FSSettingsDialog, QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)

class PMXFSPaneDock(PaneDockBase):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("File System Panel"))
        self.setWidget(FSPaneWidget(self))
