
import os

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import test_font_strategy

from prymatex.ui.configure.terminal import Ui_Terminal
from prymatex.models.settings import SettingsTreeNode
from prymatex.utils.i18n import ugettext as _
from prymatex.widgets.pmxterm.schemes import ColorScheme

class TerminalSettingsWidget(SettingsTreeNode, Ui_Terminal, QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super(TerminalSettingsWidget, self).__init__(nodeName = "terminal", **kwargs)
        self.setupUi(self)
        self.setTitle("Terminal")
        self.setIcon(self.resources().get_icon("settings-terminal"))

    def loadSettings(self):
        super(TerminalSettingsWidget, self).loadSettings()
        defaultScheme = self.settings.value('defaultScheme')
        
        for index, scheme in enumerate(ColorScheme.SCHEMES):
            self.comboBoxScheme.addItem(scheme.name)
            if defaultScheme == scheme.name:
                self.comboBoxScheme.setCurrentIndex(index)
        
        editorTheme = self.settings.value('editorTheme')
        self.checkBoxEditorTheme.setChecked(editorTheme)
        self.comboBoxScheme.setDisabled(editorTheme)

        # Font
        defaultFont = self.settings.value('defaultFont')
        self.fontComboBoxName.setCurrentFont(defaultFont)
        self.spinBoxFontSize.setValue(defaultFont.pointSize())
        self.checkBoxAntialias.setChecked(test_font_strategy(defaultFont, QtGui.QFont.PreferAntialias))
        
        self.checkBoxSynchronize.setChecked(self.settings.value('synchronizeEditor'))
        self.spinBoxBufferSize.setValue(self.settings.value('bufferSize'))
        
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
        self.settings.setValue('defaultFont', font)

    def setSynchronizeEditorSetting(self, state):
        self.settings.setValue('synchronizeEditor', state == QtCore.Qt.Checked)
        
    def setEditorThemeSetting(self, state):
        self.comboBoxScheme.setDisabled(state == QtCore.Qt.Checked)
        self.settings.setValue('editorTheme', state == QtCore.Qt.Checked)

    @QtCore.Slot(str)
    def on_comboBoxScheme_activated(self, name):
        self.settings.setValue('defaultScheme', name)

    @QtCore.Slot()
    def on_pushButtonChangeFont_pressed(self):
        font = self.settings.value('font')
        font, ok = QtWidgets.QFontDialog.getFont(font, self, _("Select terminal font"))
        if ok:
            self.settings.setValue('font', font)
            self.comboBoxFontName.setCurrentFont(font)
            self.spinBoxFontSize.setValue(font.pointSize())
    
    
