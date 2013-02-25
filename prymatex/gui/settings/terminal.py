
import os

from prymatex.qt import QtGui, QtCore

from prymatex import resources

from prymatex.ui.configure.terminal import Ui_Terminal
from prymatex.models.settings import SettingsTreeNode
from prymatex.utils.i18n import ugettext as _
from prymatex.widgets.pmxterm.schemes import ColorScheme

class PMXTerminalSettings(QtGui.QWidget, SettingsTreeNode, Ui_Terminal):
    TITLE = "Terminal"
    ICON = resources.getIcon("utilities-terminal")
    
    def __init__(self, settingGroup, profile = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "terminal", settingGroup, profile)
        self.setupUi(self)
        
        
    def loadSettings(self):
        SettingsTreeNode.loadSettings(self)
        defaultScheme = self.settingGroup.value('defaultScheme')
        
        for index, scheme in enumerate(ColorScheme.SCHEMES):
            self.comboBoxScheme.addItem(scheme.name)
            if defaultScheme == scheme.name:
                self.comboBoxScheme.setCurrentIndex(index)
                
        font = self.settingGroup.value('defaultFont')
        self.comboBoxFontName.setCurrentFont(font)
        self.spinBoxFontSize.setValue(font.pointSize())
        
        self.checkBoxEditorTheme.blockSignals(True)
        self.checkBoxEditorTheme.setChecked(self.settingGroup.value('editorTheme'))
        self.checkBoxEditorTheme.blockSignals(False)


    @QtCore.pyqtSlot(str)
    def on_comboBoxScheme_activated(self, name):
        self.settingGroup.setValue('defaultScheme', name)


    @QtCore.pyqtSlot()
    def on_pushButtonChangeFont_pressed(self):
        font = self.settingGroup.value('font')
        font, ok = QtGui.QFontDialog.getFont(font, self, _("Select terminal font"))
        if ok:
            self.settingGroup.setValue('font', font)
            self.comboBoxFontName.setCurrentFont(font)
            self.spinBoxFontSize.setValue(font.pointSize())
    
    @QtCore.pyqtSlot(int)
    def on_checkBoxEditorTheme_stateChanged(self, state):
        self.settingGroup.setValue('editorTheme', state == QtCore.Qt.Checked)
    