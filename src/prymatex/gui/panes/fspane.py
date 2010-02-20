from PyQt4.QtGui import *
from PyQt4.QtCore import *
from prymatex.gui.panes import PaneDockBase
import shutil
import os
from os.path import abspath, join, dirname, isdir, isfile, basename
from prymatex.lib.i18n import ugettext as _
from prymatex.gui.utils import createButton, addActionsToMenu
from ui_fssettings import Ui_FSSettingsDialog
from prymatex.gui.panes.ui_fspane import Ui_FSPane
#from pr

#class QActionPushButton(QPushButton):
#    
#    def __init__(self, action):
#        assert isinstance(action, QAction)
#        QPushButton.__init__(self)
#        self._action = action
#        self.copyParams()
#        self.connect(self, SIGNAL("pressed()"), self._action, SLOT("trigger()"))
#        
#    def copyParams(self):
#        self.setText(self._action.text())
##        setTextOrig = self._action.setText
#        self.setIcon(self._action.icon())
#        self.setToolTip(self._action.toolTip())
#    


class FSPaneWidget(QWidget, Ui_FSPane):
    
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setObjectName('FSPaneWidget')
        self.dialogConfigFilters = PMXFSPaneConfigDialog(self)
        self.setupUi(self)
        start_dir = qApp.instance().startDirectory()
        self.tree.setRootIndex(self.tree.model().index(start_dir))
#        
#    def setupGui(self):
#        mainlayout = QVBoxLayout()
#        layoutButtons = QHBoxLayout()
#        layoutButtons.setObjectName('layoutButtons')
#        # Oneliner Watchout!! Sorry
#        self.actionUp = QAction(_("Up"), self)
#        self.actionUp.setObjectName('actionUp')
#        self.buttonUp = QActionPushButton(self.actionUp)
#        self.buttonUp.setObjectName('buttonUp')
#        layoutButtons.addWidget(self.buttonUp)
#        
#        self.buttonFilter = QPushButton(_("F"), self)
#        self.buttonFilter.setObjectName("buttonFilter")
#        self.buttonFilter.setToolTip("Filter Settings")
#        layoutButtons.addWidget(self.buttonFilter)
#        
#        self.buttonSyncTabFile = QPushButton(_("S"), self)
#        self.buttonSyncTabFile.setToolTip(_("Sync opened file"))
#        self.buttonSyncTabFile.setObjectName("buttonSyncTabFile")
#        # Keeping it simple
#        #self.buttonSyncTabFile.setCheckable(True)
#        layoutButtons.addWidget(self.buttonSyncTabFile)
#        self.setMaximumWidth(200)
#        
#        self.buttonBackRoot = QPushButton(_("<-"), self)
#        self.buttonBackRoot.setToolTip(_("Back to previous location"))
#        self.buttonBackRoot.setEnabled(False)
#        self.buttonBackRoot.setObjectName("buttonBackRoot")
#        layoutButtons.addWidget(self.buttonBackRoot)
#        
#        self.buttonNextRoot = QPushButton(_("->"), self)
#        self.buttonNextRoot.setToolTip(_("Next location"))
#        self.buttonNextRoot.setObjectName("buttonNextkRoot")
#        layoutButtons.addWidget(self.buttonNextRoot)  
#        
#        self.buttonCollapseAll = QPushButton(_("-"), self)
#        self.buttonCollapseAll.setObjectName("buttonCollapseAll")
#        self.buttonCollapseAll.setToolTip(_("Collapse All"))
#        layoutButtons.addWidget(self.buttonCollapseAll)
#        
#        layoutButtons.addStretch(1)
#        
#        mainlayout.addLayout(layoutButtons)
#        self.tree = FSTree(self)
#        
#        mainlayout.addWidget(self.tree)
#        self.setLayout(mainlayout)
        
#        self.setStyleSheet('''
#            QPushButton {
#            }
#        ''')
    
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


