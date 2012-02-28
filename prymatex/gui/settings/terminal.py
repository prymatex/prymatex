
import os

from PyQt4 import QtGui, QtCore
from PyQt4.QtNetwork import QNetworkProxy

from prymatex.ui.configure.terminal import Ui_Terminal
from prymatex.gui.settings.models import PMXSettingTreeNode
from prymatex.utils.i18n import ugettext as _
from prymatex import resources
class PMXTerminalSettings(QtGui.QWidget, PMXSettingTreeNode, Ui_Terminal):
    
    #NAMESPACE = "Dockers.Dockeantes"
    TITLE = "Terminal"
    ICON = resources.getIcon('terminal') 
    
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PMXSettingTreeNode.__init__(self, "terminal", settingGroup)
        self.setupUi(self)
        
        try:
            from QTermWidget import QTermWidget
        except ImportError:
            return
        
        t = QTermWidget()
        
        
        self.comboScrollBar.addItem(_("No scrollbar"), t.NoScrollBar)
        self.comboScrollBar.addItem(_("Left scrollbar"), t.ScrollBarLeft)
        self.comboScrollBar.addItem(_("Right scrollbar"), t.ScrollBarRight)
        
        for name in t.availableColorSchemes():
            self.comboColorScheme.addItem(name, name)
        
        del t
        
        
    
    
    