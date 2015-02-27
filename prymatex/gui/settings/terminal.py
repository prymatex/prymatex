
import os

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import test_font_strategy

from prymatex.ui.configure.terminal import Ui_Terminal
from prymatex.models.settings import SettingsTreeNode
from prymatex.utils.i18n import ugettext as _
from prymatex.widgets.pmxterm.schemes import ColorScheme

class TerminalSettingsWidget(SettingsTreeNode, Ui_Terminal, QtWidgets.QWidget):
    def __init__(self, component_class, **kwargs):
        super(TerminalSettingsWidget, self).__init__(component_class, nodeName = "terminal", **kwargs)
        self.setupUi(self)

    def loadSettings(self):
        super(TerminalSettingsWidget, self).loadSettings()
        self.setTitle("Terminal")
        self.setIcon(self.application().resources().get_icon("settings-terminal"))
        defaultScheme = self.settings().get('defaultScheme')
        
        for index, scheme in enumerate(ColorScheme.SCHEMES):
            self.comboBoxScheme.addItem(scheme.name)
            if defaultScheme == scheme.name:
                self.comboBoxScheme.setCurrentIndex(index)
        
        editorTheme = self.settings().get('editorTheme')
        self.checkBoxEditorTheme.setChecked(editorTheme)
        self.comboBoxScheme.setDisabled(editorTheme)

        # Font
        defaultFont = self.settings().get('defaultFont')
        self.fontComboBoxName.setCurrentFont(defaultFont)
        self.spinBoxFontSize.setValue(defaultFont.pointSize())
        self.checkBoxAntialias.setChecked(test_font_strategy(defaultFont, QtGui.QFont.PreferAntialias))
        
        self.checkBoxSynchronize.setChecked(self.settings().get('synchronizeEditor'))
        self.spinBoxBufferSize.setValue(self.settings().get('bufferSize'))
        
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
        self.settings().set('defaultFont', font)

    def setSynchronizeEditorSetting(self, state):
        self.settings().set('synchronizeEditor', state == QtCore.Qt.Checked)
        
    def setEditorThemeSetting(self, state):
        self.comboBoxScheme.setDisabled(state == QtCore.Qt.Checked)
        self.settings().set('editorTheme', state == QtCore.Qt.Checked)

    @QtCore.Slot(str)
    def on_comboBoxScheme_activated(self, name):
        self.settings().set('defaultScheme', name)

    @QtCore.Slot()
    def on_pushButtonChangeFont_pressed(self):
        font = self.settings().get('font')
        font, ok = QtWidgets.QFontDialog.getFont(font, self, _("Select terminal font"))
        if ok:
            self.settings().set('font', font)
            self.comboBoxFontName.setCurrentFont(font)
            self.spinBoxFontSize.set(font.pointSize())
    
    
