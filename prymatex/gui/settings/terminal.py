
import os

from prymatex.qt import QtGui, QtCore

from prymatex.ui.configure.terminal import Ui_Terminal
from prymatex.models.settings import SettingsTreeNode
from prymatex.utils.i18n import ugettext as _
from prymatex import resources

class PMXTerminalSettings(QtGui.QWidget, SettingsTreeNode, Ui_Terminal):
    TITLE = "Terminal"
    ICON = resources.getIcon("utilities-terminal")
    
    def __init__(self, settingGroup, profile = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "terminal", settingGroup, profile)
        self.setupUi(self)
        
        
    def loadSettings(self):
        SettingsTreeNode.loadSettings(self)
        #colorScheme = self.settingGroup.value('colorScheme')
        #self.comboColorScheme.setCurrentIndex(self.comboColorScheme.findData(colorScheme))    
        font = self.settingGroup.value('font')
        self.comboBoxFontName.setCurrentFont(font)
        self.spinBoxFontSize.setValue(font.pointSize())


    @QtCore.pyqtSlot(int)
    def on_comboColorScheme_activated(self, index):
        scheme = self.comboColorScheme.itemData(index)
        self.settingGroup.setValue('colorScheme', scheme)


    @QtCore.pyqtSlot()
    def on_pushButtonChangeFont_pressed(self):
        font = self.settingGroup.value('font')
        font, ok = QtGui.QFontDialog.getFont(font, self, _("Select terminal font"))
        if ok:
            self.settingGroup.setValue('font', font)
            self.comboBoxFontName.setCurrentFont(font)
            self.spinBoxFontSize.setValue(font.pointSize())