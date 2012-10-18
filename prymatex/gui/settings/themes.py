#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex import resources

from prymatex.ui.configure.theme import Ui_FontThemeWidget
from prymatex.gui.settings.models import PMXSettingTreeNode
from prymatex.models.delegates import PMXColorDelegate, PMXFontStyleDelegate
from prymatex.gui.support.qtadapter import QColor2RGBA
from prymatex.utils.i18n import ugettext as _

class PMXThemeWidget(QtGui.QWidget, PMXSettingTreeNode, Ui_FontThemeWidget):
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
                             'selection': '#A6CBFF' },
                #Names and scopes
                'styles': [ ('Comment', 'comment'),
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
    
    def __init__(self, settingGroup, parent = None):
        QtGui.QWidget.__init__(self, parent)
        PMXSettingTreeNode.__init__(self, "theme", settingGroup)
        self.setupUi(self)
        self.setupTableView()
        self.setupPushButton()
    
    def loadSettings(self):
        currentThemeUUID = self.settingGroup.hasValue('theme') and self.settingGroup.value('theme').upper() or None 
        currentTheme = self.application.supportManager.getTheme(currentThemeUUID)
        self.tableView.setModel(self.application.supportManager.themeStyleProxyModel)
        self.comboBoxThemes.setModel(self.application.supportManager.themeListModel)
        if currentTheme is not None:
            self.comboBoxThemes.setCurrentIndex(self.comboBoxThemes.model().findIndex(currentTheme))
            self.setThemeSettings(currentTheme, False)
    
    #==========================================================
    # ComboBoxThemes
    #==========================================================
    @QtCore.pyqtSlot(int)
    def on_comboBoxThemes_activated(self, index):
        theme = self.comboBoxThemes.model().themeForIndex(index)
        self.setThemeSettings(theme)
        
    #==========================================================
    # TableView
    #==========================================================
    def on_tableView_Activated(self, index):
        style = self.application.supportManager.themeStyleProxyModel.mapToSource(index).internalPointer()
        self.comboBoxScope.setEditText(style.scope) 
    
    def on_comboBoxScope_changed(self, string):
        string = unicode(string)
        index = self.tableView.currentIndex()
        if index.isValid():
            style = self.application.supportManager.themeStyleProxyModel.mapToSource(index).internalPointer()
            if string != style.scope:
                self.application.supportManager.updateThemeStyle(style, scope = string)

    def setupTableView(self):
        self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableView.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        
        self.tableView.activated.connect(self.on_tableView_Activated)
        self.tableView.pressed.connect(self.on_tableView_Activated)
        self.tableView.setItemDelegateForColumn(1, PMXColorDelegate(self))
        self.tableView.setItemDelegateForColumn(2, PMXColorDelegate(self))
        self.tableView.setItemDelegateForColumn(3, PMXFontStyleDelegate(self))
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        
        #Conectar
        for _, scope in self.DEFAULTS['styles']:
            self.comboBoxScope.addItem(scope)
        self.comboBoxScope.currentIndexChanged[str].connect(self.on_comboBoxScope_changed)
        self.comboBoxScope.editTextChanged.connect(self.on_comboBoxScope_changed)
    
    #==========================================================
    # Push Button
    #==========================================================
    def setupPushButton(self):
        #Colors
        self.pushButtonForeground.pressed.connect(lambda element = 'foreground': self.on_pushButtonColor_pressed(element))
        self.pushButtonBackground.pressed.connect(lambda element = 'background': self.on_pushButtonColor_pressed(element))
        self.pushButtonSelection.pressed.connect(lambda element = 'selection': self.on_pushButtonColor_pressed(element))
        self.pushButtonInvisibles.pressed.connect(lambda element = 'invisibles': self.on_pushButtonColor_pressed(element))
        self.pushButtonLineHighlight.pressed.connect(lambda element = 'lineHighlight': self.on_pushButtonColor_pressed(element))
        self.pushButtonCaret.pressed.connect(lambda element = 'caret': self.on_pushButtonColor_pressed(element))
        self.pushButtonGutter.pressed.connect(lambda element = 'gutter': self.on_pushButtonColor_pressed(element))
        #Font
        font = self.settingGroup.value('font')
        if font is not None:
            self.lineFont.setFont(font)
            self.lineFont.setText("%s, %d" % (font.family(), font.pointSize()))
    
    @QtCore.pyqtSignature('')
    def on_pushButtonChangeFont_pressed(self):
        font = self.settingGroup.value('font')
        font, ok = QtGui.QFontDialog.getFont(font, self, _("Select editor font"))
        if ok:
            self.settingGroup.setValue('font', font)
            self.lineFont.setFont(font)
            self.lineFont.setText("%s, %d" % (font.family(), font.pointSize()))
    
    @QtCore.pyqtSignature('')
    def on_pushButtonAdd_pressed(self):
        theme = self.comboBoxThemes.model().themeForIndex(self.comboBoxThemes.currentIndex())
        style = self.application.supportManager.createThemeStyle('untitled', unicode(self.comboBoxScope.currentText()), theme)
    
    @QtCore.pyqtSignature('')
    def on_pushButtonRemove_pressed(self):
        index = self.tableView.currentIndex()
        if index.isValid():
            style = self.application.supportManager.themeStyleProxyModel.mapToSource(index).internalPointer()
            self.application.supportManager.deleteThemeStyle(style)
    
    def on_pushButtonColor_pressed(self, element):
        theme = self.comboBoxThemes.model().themeForIndex(self.comboBoxThemes.currentIndex())
        settings = theme.settings
        color, ok = QtGui.QColorDialog.getRgba(settings[element].rgba(), self)
        if ok:
            self.application.supportManager.updateTheme(theme, settings = { element: color })
            self.setThemeSettings(theme)
    
    def setThemeSettings(self, theme, changeSettings = True):
        settings = theme.settings
        self.pushButtonForeground.setStyleSheet("background-color: " + QColor2RGBA(settings['foreground'])[:7])
        self.pushButtonBackground.setStyleSheet("background-color: " + QColor2RGBA(settings['background'])[:7])
        self.pushButtonSelection.setStyleSheet("background-color: " + QColor2RGBA(settings['selection'])[:7])
        self.pushButtonInvisibles.setStyleSheet("background-color: " + QColor2RGBA(settings['invisibles'])[:7])
        self.pushButtonLineHighlight.setStyleSheet("background-color: " + QColor2RGBA(settings['lineHighlight'])[:7])
        self.pushButtonCaret.setStyleSheet("background-color: " + QColor2RGBA(settings['caret'])[:7])
        if 'gutter' in settings:
            #Not all themes has the gutter color
            self.pushButtonGutter.setStyleSheet("background-color: " + QColor2RGBA(settings['gutter'])[:7])
        self.application.supportManager.themeStyleProxyModel.setFilterRegExp(unicode(theme.uuid))
        
        #Set color for table view
        tableStyle = """QTableView {background-color: %s;
        color: %s;
        selection-background-color: %s; }""" % (settings['background'].name(), settings['foreground'].name(), settings['selection'].name())
        self.tableView.setStyleSheet(tableStyle)
        
        if changeSettings:
            self.settingGroup.setValue('theme', unicode(theme.uuid).upper())
            message = "<b>%s</b> theme set " % theme.name
            if theme.author is not None:
                message += "<i>(by %s)</i>" % theme.author
            self.application.showMessage(message)    
        