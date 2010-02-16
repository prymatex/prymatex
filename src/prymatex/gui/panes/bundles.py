#-*- encoding: utf-8 -*-

from PyQt4.QtGui import *
from prymatex.lib.i18n import ugettext as _
from prymatex.gui.panes import PaneDockBase

class PMXBundleWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupGui()
    
    def setupGui(self):
        layout = QVBoxLayout()
        self.comboSelectBundleType = QComboBox(self)
        self.comboSelectBundleType.addItem("Syntax")
        self.comboSelectBundleType.addItem("Snippet")
        self.comboSelectBundleType.addItem("Command")
        self.comboSelectBundleType.addItem("Preferences")
        layout.addWidget(self.comboSelectBundleType)
        layout.addWidget(QTreeView())
        
        
        layoutButtons = QHBoxLayout()
        self.buttonAdd = QPushButton(_("Add"), self)
        self.buttonAdd.setObjectName("buttonAdd")
        layoutButtons.addWidget(self.buttonAdd)
        
        self.buttonRemove = QPushButton(_("Remove"), self)
        self.buttonRemove.setObjectName("buttonRemove")
        layoutButtons.addWidget(self.buttonRemove)
        
        self.buttonManage = QPushButton(_("Manage"), self)
        self.buttonManage.setObjectName("buttonMange")
        layoutButtons.addWidget(self.buttonManage)
        layoutButtons.addStretch(-1)
        
        layout.addLayout(layoutButtons)
        self.setLayout(layout)
        
    
class PMXBundleEditorDock(PaneDockBase):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Bundles"))
        self.setWidget(PMXBundleWidget(self))
        