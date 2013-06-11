
import os

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import test_font_strategy
from prymatex import resources

from prymatex.ui.configure.terminal import Ui_Terminal
from prymatex.models.settings import SettingsTreeNode
from prymatex.utils.i18n import ugettext as _
from prymatex.widgets.pmxterm.schemes import ColorScheme

class TerminalSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_Terminal):
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
        
        editorTheme = self.settingGroup.value('editorTheme')
        self.checkBoxEditorTheme.setChecked(editorTheme)
        self.comboBoxScheme.setDisabled(editorTheme)

        # Font
        defaultFont = self.settingGroup.value('defaultFont')
        self.fontComboBoxName.setCurrentFont(defaultFont)
        self.spinBoxFontSize.setValue(defaultFont.pointSize())
        self.checkBoxAntialias.setChecked(test_font_strategy(defaultFont, QtGui.QFont.PreferAntialias))
        
        self.checkBoxSynchronize.setChecked(self.settingGroup.value('synchronizeEditor'))
        self.spinBoxBufferSize.setValue(self.settingGroup.value('bufferSize'))
        
        # Connect font signals
        self.checkBoxAntialias.stateChanged[int].connect(self.setDefaultFontSetting)
        self.checkBoxEditorTheme.stateChanged[int].connect(self.setEditorThemeSetting)
        self.checkBoxSynchronize.stateChanged[int].connect(self.setSynchronizeEditorSetting)
        self.spinBoxFontSize.valueChanged[int].connect(self.setDefaultFontSetting)
        self.fontComboBoxName.activated.connect(self.setDefaultFontSetting)


    # ---------------------- Set Settings
    def setDefaultFontSetting(self):
        font = self.fontComboBoxName.currentFont()
        font.setPointSize(self.spinBoxFontSize.value())
        if self.checkBoxAntialias.isChecked():
            font.setStyleStrategy(font.styleStrategy() | QtGui.QFont.PreferAntialias)
        self.settingGroup.setValue('defaultFont', font)

    def setSynchronizeEditorSetting(self, state):
        self.settingGroup.setValue('synchronizeEditor', state == QtCore.Qt.Checked)
        
    def setEditorThemeSetting(self, state):
        self.comboBoxScheme.setDisabled(state == QtCore.Qt.Checked)
        self.settingGroup.setValue('editorTheme', state == QtCore.Qt.Checked)

    @QtCore.Slot(str)
    def on_comboBoxScheme_activated(self, name):
        self.settingGroup.setValue('defaultScheme', name)


    @QtCore.Slot()
    def on_pushButtonChangeFont_pressed(self):
        font = self.settingGroup.value('font')
        font, ok = QtGui.QFontDialog.getFont(font, self, _("Select terminal font"))
        if ok:
            self.settingGroup.setValue('font', font)
            self.comboBoxFontName.setCurrentFont(font)
            self.spinBoxFontSize.setValue(font.pointSize())
    
    