#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui
from prymatex.qt.helpers import test_font_strategy
from prymatex.qt.helpers.colors import color2rgba

from prymatex import resources
from prymatex.ui.configure.theme import Ui_FontTheme
from prymatex.utils.i18n import ugettext as _

from prymatex.support.theme import DEFAULT_THEME_SETTINGS, DEFAULT_SCOPE_SELECTORS

from prymatex.models.settings import SettingsTreeNode
from prymatex.delegates.theme import FontStyleDelegate, ColorDelegate

class ThemeSettingsWidget(SettingsTreeNode, Ui_FontTheme, QtGui.QWidget):
    """Changes font and theme"""
    NAMESPACE = "editor"
    TITLE = "Appearance"
    ICON = resources.getIcon("fill-color")

    def __init__(self, **kwargs):
        super(ThemeSettingsWidget, self).__init__(nodeName = "theme", **kwargs)
        self.setupUi(self)
        self.setupTableView()
        self.setupPushButton()

    def loadSettings(self):
        super(ThemeSettingsWidget, self).loadSettings()
        # Set models
        self.comboBoxThemes.setModel(self.application.supportManager.themeListModel)
        self.tableViewStyles.setModel(self.application.supportManager.themeStyleProxyModel)
        
        currentThemeUUID = self.settings.value('defaultTheme')
        currentTheme = self.application.supportManager.getTheme(currentThemeUUID)
        if currentTheme is not None:
            self.updateUi(currentTheme)
        
        # Font
        font = self.settings.value('defaultFont')
        self.fontComboBoxName.setCurrentFont(QtGui.QFont(*font))
        self.spinBoxFontSize.setValue(font[1])
        #self.checkBoxAntialias.setChecked(test_font_strategy(font, QtGui.QFont.PreferAntialias))
        
        # Connect font signals
        self.checkBoxAntialias.stateChanged.connect(self.setDefaultFontSetting)
        self.spinBoxFontSize.valueChanged[int].connect(self.setDefaultFontSetting)
        self.fontComboBoxName.activated.connect(self.setDefaultFontSetting)

    # ---------------------- Set Settings
    def setDefaultFontSetting(self):
        # TODO Un dict ? en lugar de una tupla
        font = self.fontComboBoxName.currentFont()
        if self.checkBoxAntialias.isChecked():
            pass
            #font.setStyleStrategy(font.styleStrategy() | QtGui.QFont.PreferAntialias)
        self.settings.setValue('defaultFont', 
            ( self.fontComboBoxName.currentFont().family(), 
              self.spinBoxFontSize.value())
        )

    # ---------------------- Themes
    @QtCore.Slot(int)
    def on_comboBoxThemes_activated(self, index):
        theme = self.comboBoxThemes.model().themeForIndex(index)
        self.updateUi(theme)
        self.settings.setValue('defaultTheme', str(theme.uuid))
        message = "<b>%s</b> theme set " % theme.name
        if theme.author is not None:
            message += "<i>(by %s)</i>" % theme.author
        self.application.showMessage(message)

    def updateUi(self, theme):
        self.comboBoxThemes.setCurrentIndex(self.comboBoxThemes.model().findIndex(theme))    
        settings = theme.settings()
        self.pushButtonForeground.setStyleSheet("background-color: " + color2rgba(settings['foreground'])[:7])
        self.pushButtonBackground.setStyleSheet("background-color: " + color2rgba(settings['background'])[:7])
        self.pushButtonSelection.setStyleSheet("background-color: " + color2rgba(settings['selection'])[:7])
        self.pushButtonInvisibles.setStyleSheet("background-color: " + color2rgba(settings['invisibles'])[:7])
        self.pushButtonLineHighlight.setStyleSheet("background-color: " + color2rgba(settings['lineHighlight'])[:7])
        self.pushButtonCaret.setStyleSheet("background-color: " + color2rgba(settings['caret'])[:7])
        self.pushButtonGutterBackground.setStyleSheet("background-color: " + color2rgba(settings['gutterBackground'])[:7])
        self.pushButtonGutterForeground.setStyleSheet("background-color: " + color2rgba(settings['gutterForeground'])[:7])
        self.application.supportManager.themeStyleProxyModel.setFilterRegExp(str(theme.uuid))

        #Set color for table view
        tableStyle = """QTableView {background-color: %s;
        color: %s;
        selection-background-color: %s; }""" % (settings['background'].name(), settings['foreground'].name(), settings['selection'].name())
        self.tableViewStyles.setStyleSheet(tableStyle)
        self.tableViewStyles.resizeColumnsToContents()
        self.tableViewStyles.resizeRowsToContents()
        self.tableViewStyles.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)

    # --------------------- TableView
    def setupTableView(self):
        self.tableViewStyles.activated.connect(self.on_tableView_activatedOrPressed)
        self.tableViewStyles.pressed.connect(self.on_tableView_activatedOrPressed)
        
        self.tableViewStyles.setItemDelegateForColumn(1, ColorDelegate(self))
        self.tableViewStyles.setItemDelegateForColumn(2, ColorDelegate(self))
        self.tableViewStyles.setItemDelegateForColumn(3, FontStyleDelegate(self))
        self.tableViewStyles.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)

        # Combo default scope selectors
        for _, scope in DEFAULT_SCOPE_SELECTORS:
            self.comboBoxScope.addItem(scope)
        self.comboBoxScope.currentIndexChanged[str].connect(self.on_comboBoxScope_changed)
        self.comboBoxScope.editTextChanged.connect(self.on_comboBoxScope_changed)

    def on_tableView_activatedOrPressed(self, index):
        style = self.application.supportManager.themeStyleProxyModel.style(index)
        self.comboBoxScope.setEditText(style.scope)

    def on_comboBoxScope_changed(self, scopeText):
        index = self.tableViewStyles.currentIndex()
        if index.isValid():
            style = self.application.supportManager.themeStyleProxyModel.style(index)
            if scopeText != style.scope:
                self.application.supportManager.updateThemeStyle(style, scope = scopeText)

    def on_pushButtonAdd_pressed(self):
        theme = self.comboBoxThemes.model().themeForIndex(self.comboBoxThemes.currentIndex())
        self.application.supportManager.createThemeStyle(theme, scope = str(self.comboBoxScope.currentText()))

    def on_pushButtonRemove_pressed(self):
        index = self.tableViewStyles.currentIndex()
        if index.isValid():
            style = self.application.supportManager.themeStyleProxyModel.mapToSource(index).internalPointer()
            self.application.supportManager.deleteThemeStyle(style)

    # -------------------- Colors Push Button
    def setupPushButton(self):
        self.pushButtonForeground.pressed.connect(lambda element='foreground': self.on_pushButtonColor_pressed(element))
        self.pushButtonBackground.pressed.connect(lambda element='background': self.on_pushButtonColor_pressed(element))
        self.pushButtonSelection.pressed.connect(lambda element='selection': self.on_pushButtonColor_pressed(element))
        self.pushButtonInvisibles.pressed.connect(lambda element='invisibles': self.on_pushButtonColor_pressed(element))
        self.pushButtonLineHighlight.pressed.connect(lambda element='lineHighlight': self.on_pushButtonColor_pressed(element))
        self.pushButtonCaret.pressed.connect(lambda element='caret': self.on_pushButtonColor_pressed(element))
        self.pushButtonGutterBackground.pressed.connect(lambda element='gutterBackground': self.on_pushButtonColor_pressed(element))
        self.pushButtonGutterForeground.pressed.connect(lambda element='gutterForeground': self.on_pushButtonColor_pressed(element))

    def on_pushButtonColor_pressed(self, element):
        theme = self.comboBoxThemes.model().themeForIndex(self.comboBoxThemes.currentIndex())
        settings = theme.settings()
        color, ok = QtGui.QColorDialog.getRgba(settings[element].rgba(), self)
        if ok:
            self.application.supportManager.updateTheme(theme, settings = { element: color })
            self.updateUi(theme)
