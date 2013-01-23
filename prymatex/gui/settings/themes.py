#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui
from prymatex.qt.helpers import test_font_strategy

from prymatex import resources

from prymatex.ui.configure.theme import Ui_FontTheme
from prymatex.models.settings import SettingsTreeNode
from prymatex.delegates.theme import FontStyleDelegate, ColorDelegate
from prymatex.qt.helpers.colors import color2rgba
from prymatex.utils.i18n import ugettext as _


class ThemeSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_FontTheme):
    """Changes font and theme
    """
    DEFAULTS = {'settings': {'background': '#FFFFFF',
                             'caret': '#000000',
                             'foreground': '#000000',
                             'invisibles': '#BFBFBF',
                             'lineHighlight': '#00000012',
                             'gutter': '#FFFFFF',
                             'gutterForeground': '#000000',
                             'lineHighlight': '#00000012',
                             'selection': '#A6CBFF'},
                #Names and scopes
                'styles': [('Comment', 'comment'),
                           ('String', 'string'),
                           ('Number', 'constant.numeric'),
                           ('Built-in constant', 'constant.language'),
                           ('User-defined constant', 'constant.character, constant.other'),
                           ('Variable', 'variable.language, variable.other'),
                           ('Keyword', 'keyword'),
                           ('Storage', 'storage'),
                           ('Class name', 'entity.name.class'),
                           ('Inherited class', 'entity.other.inherited-class'),
                           ('Function name', 'entity.name.function'),
                           ('Function argument', 'variable.parameter'),
                           ('Tag name', 'entity.name.tag'),
                           ('Tag attribute', 'entity.other.attribute-name'),
                           ('Library function', 'support.function'),
                           ('Library constant', 'support.constant'),
                           ('Library class/type', 'support.type, support.class'),
                           ('Library variable', 'support.other.variable'),
                           ('Invalid', 'invalid')]
                }

    NAMESPACE = "editor"
    TITLE = "Font and Themes"
    ICON = resources.getIcon("fill-color")

    def __init__(self, settingGroup, parent=None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "theme", settingGroup)
        self.setupUi(self)
        self.setupTableView()
        self.setupPushButton()


    def loadSettings(self):
        # Set models
        self.comboBoxThemes.setModel(self.application.supportManager.themeListModel)
        self.tableViewStyles.setModel(self.application.supportManager.themeStyleProxyModel)
        
        currentThemeUUID = self.settingGroup.value('defaultTheme')
        currentTheme = self.application.supportManager.getTheme(currentThemeUUID)
        if currentTheme is not None:
            self.updateUi(currentTheme)
        
        # Font
        font = self.settingGroup.value('defaultFont')
        self.fontComboBoxName.setCurrentFont(font)
        self.spinBoxFontSize.setValue(font.pointSize())
        self.checkBoxAntialias.setChecked(test_font_strategy(font, QtGui.QFont.PreferAntialias))
        
        # Connect font signals
        self.checkBoxAntialias.stateChanged.connect(self.setDefaultFontSetting)
        self.spinBoxFontSize.valueChanged[int].connect(self.setDefaultFontSetting)
        self.fontComboBoxName.activated.connect(self.setDefaultFontSetting)


    # ---------------------- Set Settings
    def setDefaultFontSetting(self):
        font = self.fontComboBoxName.currentFont()
        font.setPointSize(self.spinBoxFontSize.value())
        if self.checkBoxAntialias.isChecked():
            font.setStyleStrategy(font.styleStrategy() | QtGui.QFont.PreferAntialias)
        self.settingGroup.setValue('defaultFont', font)


    def setDefaultThemeSetting(self, theme):
        self.settingGroup.setValue('defaultTheme', unicode(theme.uuid))
        # TODO: Ver si el mensage esta bien aca
        message = "<b>%s</b> theme set " % theme.name
        if theme.author is not None:
            message += "<i>(by %s)</i>" % theme.author
        self.application.showMessage(message)


    # ---------------------- Themes
    @QtCore.pyqtSlot(int)
    def on_comboBoxThemes_activated(self, index):
        theme = self.comboBoxThemes.model().themeForIndex(index)
        self.updateUi(theme)
        self.setDefaultThemeSetting(theme)


    def updateUi(self, theme):
        self.comboBoxThemes.setCurrentIndex(self.comboBoxThemes.model().findIndex(theme))    
        settings = theme.settings
        self.pushButtonForeground.setStyleSheet("background-color: " + color2rgba(settings['foreground'])[:7])
        self.pushButtonBackground.setStyleSheet("background-color: " + color2rgba(settings['background'])[:7])
        self.pushButtonSelection.setStyleSheet("background-color: " + color2rgba(settings['selection'])[:7])
        self.pushButtonInvisibles.setStyleSheet("background-color: " + color2rgba(settings['invisibles'])[:7])
        self.pushButtonLineHighlight.setStyleSheet("background-color: " + color2rgba(settings['lineHighlight'])[:7])
        self.pushButtonCaret.setStyleSheet("background-color: " + color2rgba(settings['caret'])[:7])
        self.pushButtonGutterBackground.setStyleSheet("background-color: " + color2rgba(settings['gutter'])[:7])
        self.pushButtonGutterForeground.setStyleSheet("background-color: " + color2rgba(settings['gutterForeground'])[:7])
        self.application.supportManager.themeStyleProxyModel.setFilterRegExp(unicode(theme.uuid))

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

        # Combo default scopes
        for _, scope in self.DEFAULTS['styles']:
            self.comboBoxScope.addItem(scope)
        self.comboBoxScope.currentIndexChanged[str].connect(self.on_comboBoxScope_changed)
        self.comboBoxScope.editTextChanged.connect(self.on_comboBoxScope_changed)


    def on_tableView_activatedOrPressed(self, index):
        style = self.application.supportManager.themeStyleProxyModel.style(index)
        self.comboBoxScope.setEditText(style.scope)


    def on_comboBoxScope_changed(self, string):
        index = self.tableViewStyles.currentIndex()
        if index.isValid():
            style = self.application.supportManager.themeStyleProxyModel.style(index)
            if string != style.scope:
                self.application.supportManager.updateThemeStyle(style, scope = string)


    def on_pushButtonAdd_pressed(self):
        theme = self.comboBoxThemes.model().themeForIndex(self.comboBoxThemes.currentIndex())
        self.application.supportManager.createThemeStyle('untitled', unicode(self.comboBoxScope.currentText()), theme)


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
        self.pushButtonGutterBackground.pressed.connect(lambda element='gutter': self.on_pushButtonColor_pressed(element))
        self.pushButtonGutterForeground.pressed.connect(lambda element='gutterForeground': self.on_pushButtonColor_pressed(element))


    def on_pushButtonColor_pressed(self, element):
        theme = self.comboBoxThemes.model().themeForIndex(self.comboBoxThemes.currentIndex())
        settings = theme.settings
        color, ok = QtGui.QColorDialog.getRgba(settings[element].rgba(), self)
        if ok:
            self.application.supportManager.updateTheme(theme, settings={element: color})
            self.updateUi(theme)
            self.setDefaultThemeSetting(theme)
