#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from prymatex.gui.settings.widgets import PMXConfigBaseWidget
from prymatex.core.base import PMXObject
from prymatex.models.delegates import PMXColorDelegate, PMXFontStyleDelegate
from prymatex.ui.settings.themes import Ui_FontThemeConfig
from prymatex.gui.support.qtadapter import QColor2RGBA
from prymatex.utils.i18n import ugettext as _

class PMXThemeConfigWidget(PMXConfigBaseWidget, Ui_FontThemeConfig, PMXObject):
    '''
    Changes font and theme
    '''
    DEFAULTS = {'settings': {'background': '#FFFFFF',
                             'caret': '#000000',
                             'foreground': '#000000',
                             'invisibles': '#BFBFBF',
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

    def __init__(self, parent = None):
        super(PMXThemeConfigWidget, self).__init__(parent)
        self.setupUi(self)
        
        #Settings
        self.settings = self.application.settings.getGroup('CodeEditor')

        #Manager
        self.manager = self.application.supportManager
        
        self.configComboBoxThemes()
        self.configTableView()
        self.configPushButton()
    
    #==========================================================
    # ComboBoxThemes
    #==========================================================
    @QtCore.pyqtSlot(int)
    def on_comboBoxThemes_activated(self, index):
        uuid = self.comboBoxThemes.itemData(index)
        theme = self.manager.getTheme(uuid)
        self.setThemeSettings(theme)
        
    def configComboBoxThemes(self):
        #Combo Theme
        currentTheme = None
        currentThemeUUID = self.settings.hasValue('theme') and self.settings.value('theme').upper() or None 
        for theme in self.manager.getAllThemes():
            uuid = unicode(theme.uuid).upper()
            self.comboBoxThemes.addItem(theme.name, uuid)
            if uuid == currentThemeUUID:
                currentTheme = theme
        if currentTheme is not None:
            self.comboBoxThemes.setCurrentIndex(self.comboBoxThemes.findData(currentThemeUUID))
            self.setThemeSettings(currentTheme)
    
    #==========================================================
    # TableView
    #==========================================================
    def on_tableView_Activated(self, index):
        style = self.manager.themeStyleProxyModel.mapToSource(index).internalPointer()
        self.comboBoxScope.setEditText(style.scope) 
    
    def on_comboBoxScope_changed(self, string):
        string = unicode(string)
        index = self.tableView.currentIndex()
        if index.isValid():
            style = self.manager.themeStyleProxyModel.mapToSource(index).internalPointer()
            if string != style.scope:
                self.manager.updateThemeStyle(style, scope = string)
    
    def configTableView(self):
        self.tableView.setModel(self.manager.themeStyleProxyModel)
        self.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.tableView.activated.connect(self.on_tableView_Activated)
        self.tableView.pressed.connect(self.on_tableView_Activated)
        self.tableView.setItemDelegateForColumn(1, PMXColorDelegate(self))
        self.tableView.setItemDelegateForColumn(2, PMXColorDelegate(self))
        self.tableView.setItemDelegateForColumn(3, PMXFontStyleDelegate(self))
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.tableView.resizeColumnToContents(3)
        self.tableView.setColumnWidth(0, 437)
        self.tableView.setColumnWidth(1, 25)
        self.tableView.setColumnWidth(2, 25)
        #Conectar
        for _, scope in self.DEFAULTS['styles']:
            self.comboBoxScope.addItem(scope)
        self.comboBoxScope.currentIndexChanged[str].connect(self.on_comboBoxScope_changed)
        self.comboBoxScope.editTextChanged.connect(self.on_comboBoxScope_changed)
    
    #==========================================================
    # Push Button
    #==========================================================
    def configPushButton(self):
        #Colors
        self.pushButtonForeground.pressed.connect(lambda element = 'foreground': self.on_pushButtonColor_pressed(element))
        self.pushButtonBackground.pressed.connect(lambda element = 'background': self.on_pushButtonColor_pressed(element))
        self.pushButtonSelection.pressed.connect(lambda element = 'selection': self.on_pushButtonColor_pressed(element))
        self.pushButtonInvisibles.pressed.connect(lambda element = 'invisibles': self.on_pushButtonColor_pressed(element))
        self.pushButtonLineHighlight.pressed.connect(lambda element = 'lineHighlight': self.on_pushButtonColor_pressed(element))
        self.pushButtonCaret.pressed.connect(lambda element = 'caret': self.on_pushButtonColor_pressed(element))
        #Font
        font = self.settings.value('font')
        if font is not None:
            self.lineFont.setFont(font)
            self.lineFont.setText("%s, %d" % (font.family(), font.pointSize()))
    
    @QtCore.pyqtSignature('')
    def on_pushButtonChangeFont_pressed(self):
        font = self.settings.value('font')
        font, ok = QtGui.QFontDialog.getFont(font, self, _("Select editor font"))
        if ok:
            self.settings.setValue('font', font)
            self.lineFont.setFont(font)
            self.lineFont.setText("%s, %d" % (font.family(), font.pointSize()))
    
    @QtCore.pyqtSignature('')
    def on_pushButtonAdd_pressed(self):
        uuid = self.comboBoxThemes.itemData(self.comboBoxThemes.currentIndex())
        theme = self.manager.getTheme(unicode(uuid))
        style = self.manager.createThemeStyle('untitled', unicode(self.comboBoxScope.currentText()), theme)
    
    @QtCore.pyqtSignature('')
    def on_pushButtonRemove_pressed(self):
        index = self.tableView.currentIndex()
        if index.isValid():
            style = self.manager.themeStyleProxyModel.mapToSource(index).internalPointer()
            self.manager.deleteThemeStyle(style)
    
    def on_pushButtonColor_pressed(self, element):
        uuid = self.comboBoxThemes.itemData(self.comboBoxThemes.currentIndex())
        theme = self.manager.getTheme(unicode(uuid))
        settings = theme.settings
        color, ok = QtGui.QColorDialog.getRgba(settings[element].rgba(), self)
        if ok:
            self.manager.updateTheme(theme, settings = { element: color })
            self.setThemeSettings(theme)
    
    def setThemeSettings(self, theme):
        settings = theme.settings
        self.pushButtonForeground.setStyleSheet("background-color: " + QColor2RGBA(settings['foreground'])[:7])
        self.pushButtonBackground.setStyleSheet("background-color: " + QColor2RGBA(settings['background'])[:7])
        self.pushButtonSelection.setStyleSheet("background-color: " + QColor2RGBA(settings['selection'])[:7])
        self.pushButtonInvisibles.setStyleSheet("background-color: " + QColor2RGBA(settings['invisibles'])[:7])
        self.pushButtonLineHighlight.setStyleSheet("background-color: " + QColor2RGBA(settings['lineHighlight'])[:7])
        self.pushButtonCaret.setStyleSheet("background-color: " + QColor2RGBA(settings['caret'])[:7])
        self.manager.themeStyleProxyModel.setFilterRegExp(unicode(theme.uuid))
        self.settings.setValue('theme', unicode(theme.uuid))
        