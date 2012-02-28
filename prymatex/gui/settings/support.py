
import os

from PyQt4 import QtGui, QtCore
from prymatex.gui.settings.models import PMXSettingTreeNode
from prymatex.utils.i18n import ugettext as _
from prymatex import resources

class PMXSupportSettings(QtGui.QWidget, PMXSettingTreeNode, ):
    ICON = resources.getIcon('gear') 
    TITLE = "Support"
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PMXSettingTreeNode.__init__(self, "support", settingGroup)
        #self.setupUi(self)    
        print "Support" + "*" * 40