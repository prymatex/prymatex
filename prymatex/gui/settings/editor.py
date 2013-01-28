#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.editor import Ui_Editor
from prymatex.models.settings import SettingsTreeNode
from prymatex.gui.codeeditor.editor import CodeEditor
from prymatex.gui.codeeditor.sidebar import (LineNumberSideBarAddon, BookmarkSideBarAddon,
                                FoldingSideBarAddon, SelectionSideBarAddon)
    
class EditorSettingsWidget(QtGui.QWidget, SettingsTreeNode, Ui_Editor):
    TITLE = "Editor"
    ICON = resources.getIcon("accessories-text-editor")
    
    def __init__(self, settingGroup, profile = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        SettingsTreeNode.__init__(self, "editor", settingGroup, profile)
        self.setupUi(self)
        #self.checkBoxFolding.toggled.connect(self.on_gutterOption_toggled)
        #self.checkBoxBookmarks.toggled.connect(self.on_gutterOption_toggled)
        
        # Default addons groups
        self.bookmarksBarGroup = profile.groupByClass(BookmarkSideBarAddon)
        self.lineNumberBarGroup = profile.groupByClass(LineNumberSideBarAddon)
        self.foldingBarGroup = profile.groupByClass(FoldingSideBarAddon)
        self.selectionBarGroup = profile.groupByClass(SelectionSideBarAddon)


    def loadSettings(self):
        self.comboBoxDefaultSyntax.setModel(self.application.supportManager.syntaxProxyModel)
        self.comboBoxDefaultSyntax.setModelColumn(0)
        
        uuid = self.settingGroup.value('defaultSyntax')
        syntax = self.application.supportManager.getBundleItem(uuid)
        index = self.comboBoxDefaultSyntax.model().findItemIndex(syntax)
        self.comboBoxDefaultSyntax.setCurrentIndex(index)
        
        flags = int(self.settingGroup.value('defaultFlags'))
        
        self.checkBoxFolding.setChecked(self.foldingBarGroup.value("showFolding"))
        self.checkBoxBookmarks.setChecked(self.bookmarksBarGroup.value("showBookmarks"))
        self.checkBoxLineNumbers.setChecked(self.lineNumberBarGroup.value("showLineNumbers"))
        #self.checkBoxSelection.setChecked(self.bookmarksBarGroup.value())
        
        
    def on_checkBoxLineNumbers_toggled(self, checked):
        self.lineNumberBarGroup.setValue('showLineNumbers', self.checkBoxLineNumbers.isChecked())
        
    @QtCore.pyqtSlot(int)
    def on_comboBoxDefaultSyntax_activated(self, index):
        model = self.comboBoxDefaultSyntax.model()
        node = model.mapToSource(model.createIndex(index, 0))
        self.settingGroup.setValue('defaultSyntax', str(node.internalPointer().uuid).upper())
    