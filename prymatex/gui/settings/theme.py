#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import test_font_strategy
from prymatex.qt.helpers.colors import color2rgba

from prymatex.ui.configure.theme import Ui_FontTheme
from prymatex.utils.i18n import ugettext as _

from prymatex.support.bundleitem.theme import DEFAULT_THEME_SETTINGS, DEFAULT_SCOPE_SELECTORS

from prymatex.models.settings import SettingsTreeNode
from prymatex.delegates.theme import FontStyleDelegate, ColorDelegate

class ThemeSettingsWidget(SettingsTreeNode, Ui_FontTheme, QtWidgets.QWidget):
    """Changes font and theme"""
    NAMESPACE = "editor"

    def __init__(self, component_class, **kwargs):
        super(ThemeSettingsWidget, self).__init__(component_class, nodeName="theme", **kwargs)
        self.setupUi(self)
        self.setupTableView()
        self.setupPushButton()

    def loadSettings(self):
        super(ThemeSettingsWidget, self).loadSettings()
        self.setTitle("Appearance")
        self.setIcon(self.application().resources().get_icon("settings-theme"))

        # Set models
        self.comboBoxThemes.setModel(self.application().supportManager.themeProxyModel)
        self.tableViewStyles.setModel(self.application().supportManager.themeStyleProxyModel)
        
        theme_uuid = self.settings().get('default_theme')
        if theme_uuid is not None:
            default_theme = self.application().supportManager.getTheme(theme_uuid)
            if default_theme is not None:
                self.updateUi(default_theme)
        
        # Font
        default_font = self.settings().get('default_font')
        if default_font is not None:
            font = QtGui.QFont(*default_font)
            self.fontComboBoxName.setCurrentFont(font)
            self.spinBoxFontSize.setValue(default_font[1])
            self.checkBoxAntialias.setChecked(test_font_strategy(font, QtGui.QFont.PreferAntialias))
        
        # Connect font signals
        self.checkBoxAntialias.stateChanged.connect(self.setDefaultFontSetting)
        self.spinBoxFontSize.valueChanged[int].connect(self.setDefaultFontSetting)
        self.fontComboBoxName.activated.connect(self.setDefaultFontSetting)

    # ---------------------- Set Settings
    def setDefaultFontSetting(self):
        # TODO Un dict ? en lugar de una tupla
        font = self.fontComboBoxName.currentFont()
        if self.checkBoxAntialias.isChecked():
            font.setStyleStrategy(font.styleStrategy() | QtGui.QFont.PreferAntialias)
        self.settings().set('default_font', 
            ( self.fontComboBoxName.currentFont().family(), 
              self.spinBoxFontSize.value())
        )

    # ---------------------- Themes
    @QtCore.Slot(int)
    def on_comboBoxThemes_activated(self, index):
        modelIndex = self.comboBoxThemes.model().index(index)
        theme = self.comboBoxThemes.model().node(modelIndex)
        item = theme.bundleItem()
        self.updateUi(item)
        self.settings().set('default_theme', theme.uuid())
        message = "<b>%s</b> theme set " % item.name
        if item.author is not None:
            message += "<i>(by %s)</i>" % item.author
        self.application().showMessage(message)

    def updateUi(self, theme):
        node = self.application().supportManager.getManagedObjectNode(theme.uuid)
        index = self.comboBoxThemes.model().indexFromNode(node)
        self.comboBoxThemes.setCurrentIndex(index.row())
        palette = self.application().supportManager.getThemePalette(theme)
        # Filter theme proxy model
        self.application().supportManager.themeStyleProxyModel.setFilterRegExp(theme.uuidAsText())

        # Set color for table view
        self.tableViewStyles.setPalette(palette)
        self.tableViewStyles.viewport().setPalette(palette)
        self.tableViewStyles.resizeColumnsToContents()
        self.tableViewStyles.resizeRowsToContents()
        
        # Set color for buttons
        for button, name, role in self.buttons:
            p = button.palette()
            p.setColor(QtGui.QPalette.Button, palette.color(role))
            button.setPalette(p)

    # --------------------- TableView
    def setupTableView(self):
        self.tableViewStyles.activated.connect(self.on_tableView_activatedOrPressed)
        self.tableViewStyles.pressed.connect(self.on_tableView_activatedOrPressed)
        
        self.tableViewStyles.setItemDelegateForColumn(1, ColorDelegate(self))
        self.tableViewStyles.setItemDelegateForColumn(2, ColorDelegate(self))
        self.tableViewStyles.setItemDelegateForColumn(3, FontStyleDelegate(self))
        self.tableViewStyles.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)

        # Combo default scope selectors
        for _, scope in DEFAULT_SCOPE_SELECTORS:
            self.comboBoxScope.addItem(scope)
        self.comboBoxScope.currentIndexChanged[str].connect(self.on_comboBoxScope_changed)
        self.comboBoxScope.editTextChanged.connect(self.on_comboBoxScope_changed)

    def on_tableView_activatedOrPressed(self, index):
        style = self.application().supportManager.themeStyleProxyModel.style(index)
        self.comboBoxScope.setEditText(style.scope)

    def on_comboBoxScope_changed(self, scopeText):
        index = self.tableViewStyles.currentIndex()
        if index.isValid():
            style = self.application().supportManager.themeStyleProxyModel.style(index)
            if scopeText != style.scope:
                self.application().supportManager.updateThemeStyle(style, scope = scopeText)

    def on_pushButtonAdd_pressed(self):
        theme = self.comboBoxThemes.model().node(self.comboBoxThemes.currentIndex())
        self.application().supportManager.createThemeStyle(theme, scope = str(self.comboBoxScope.currentText()))

    def on_pushButtonRemove_pressed(self):
        index = self.tableViewStyles.currentIndex()
        if index.isValid():
            style = self.application().supportManager.themeStyleProxyModel.mapToSource(index).internalPointer()
            self.application().supportManager.deleteThemeStyle(style)

    # -------------------- Colors Push Button
    def setupPushButton(self):
        self.buttons = ( # Object, textmate name, Qt Role
            (self.pushButtonForeground, 'foreground', QtGui.QPalette.WindowText),
            (self.pushButtonBackground, 'background', QtGui.QPalette.Window),
            (self.pushButtonSelection, 'selection', QtGui.QPalette.Highlight),
            (self.pushButtonInvisibles, 'invisibles', QtGui.QPalette.HighlightedText),
            (self.pushButtonLineHighlight, 'lineHighlight', QtGui.QPalette.AlternateBase),
            (self.pushButtonCaret, 'caret', QtGui.QPalette.BrightText),
            (self.pushButtonGutterBackground, 'gutterBackground', QtGui.QPalette.ToolTipBase),
            (self.pushButtonGutterForeground, 'gutterForeground', QtGui.QPalette.ToolTipText)
        )
        for button, name, role in self.buttons:
            button.setAutoFillBackground(True)
            button.setFlat(True)
            button.pressed.connect(lambda element=name: self.on_pushButtonColor_pressed(element))

    def on_pushButtonColor_pressed(self, element):
        model = self.comboBoxThemes.model()
        sIndex = model.index(self.comboBoxThemes.currentIndex())
        theme = model.node(sIndex)
        settings = theme.getStyle()
        color, ok = QtWidgets.QColorDialog.getRgba(settings[element].rgba(), self)
        if ok:
            # TODO No pasar None, mejorar el uso del namespace default
            self.application().supportManager.updateBundleItem(theme, None, settings={element:color})
            self.updateUi(theme)
