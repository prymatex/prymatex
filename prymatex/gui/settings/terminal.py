
import os

from PyQt4 import QtGui, QtCore
from PyQt4.QtNetwork import QNetworkProxy

from prymatex.ui.configure.browser import Ui_BrowserWidget
from prymatex.gui.settings.models import PMXSettingTreeNode

class PMXTerminalSettings(QtGui.QWidget, PMXSettingTreeNode):
    
    NAMESPACE = "Dockers"
    TITLE = "Terminal"
    
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PMXSettingTreeNode.__init__(self, "browser", settingGroup)
        self.setupUi(self)
    