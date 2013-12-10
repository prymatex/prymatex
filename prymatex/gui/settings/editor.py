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

        self.checks = [(self.checkBoxWrapLines, CodeEditor.WordWrap),
            (self.checkBoxShowTabSpaces, CodeEditor.ShowTabsAndSpaces),
            (self.checkBoxShowLineParagraph, CodeEditor.ShowLineAndParagraphs),
            (self.checkBoxShowIndentGuide, CodeEditor.IndentGuide),
            (self.checkBoxHighlightCurrenLine, CodeEditor.HighlightCurrentLine),
            (self.checkBoxShowMarginLine, CodeEditor.MarginLine),
        ]
        
        for check, flag in self.checks:
            check.toggled.connect(self.on_editorFlags_toggled)

        # Default addons groups
        self.bookmarksBarGroup = profile.groupByClass(BookmarkSideBarAddon)
        self.lineNumberBarGroup = profile.groupByClass(LineNumberSideBarAddon)
        self.foldingBarGroup = profile.groupByClass(FoldingSideBarAddon)
        self.selectionBarGroup = profile.groupByClass(SelectionSideBarAddon)

    def loadSettings(self):
        SettingsTreeNode.loadSettings(self)
        self.comboBoxDefaultSyntax.setModel(self.application.supportManager.syntaxProxyModel)
        self.comboBoxDefaultSyntax.setModelColumn(0)
        
        uuid = self.settingGroup.value('defaultSyntax')
        syntax = self.application.supportManager.getBundleItem(uuid)
        index = self.comboBoxDefaultSyntax.model().findItemIndex(syntax)
        # TODO Ver porque no esta el valor
        if index:
            self.comboBoxDefaultSyntax.setCurrentIndex(index)
        
        # Flags
        flags = int(self.settingGroup.value('defaultFlags'))
        for check, flag in self.checks:
            check.setChecked(bool(flags & flag))

        self.spinBoxMarginLineSpace.setValue(self.settingGroup.value("marginLineSize"))
        
        self.checkBoxLineNumbers.setChecked(self.lineNumberBarGroup.value("showLineNumbers"))
        self.checkBoxBookmarks.setChecked(self.bookmarksBarGroup.value("showBookmarks"))
        self.checkBoxFolding.setChecked(self.foldingBarGroup.value("showFolding"))
        self.checkBoxSelection.setChecked(self.selectionBarGroup.value("showSelection"))

    def on_checkBoxLineNumbers_toggled(self, checked):
        self.lineNumberBarGroup.setValue('showLineNumbers', self.checkBoxLineNumbers.isChecked())

    def on_checkBoxBookmarks_toggled(self, checked):
        self.bookmarksBarGroup.setValue('showBookmarks', self.checkBoxBookmarks.isChecked())

    def on_checkBoxFolding_toggled(self, checked):
        self.foldingBarGroup.setValue('showFolding', self.checkBoxFolding.isChecked())
        
    def on_checkBoxSelection_toggled(self, checked):
        self.selectionBarGroup.setValue('showSelection', self.checkBoxSelection.isChecked())

    @QtCore.Slot(int)
    def on_spinBoxMarginLineSpace_valueChanged(self, value):
        self.settingGroup.setValue('marginLineSize', value)

    @QtCore.Slot(int)
    def on_comboBoxDefaultSyntax_activated(self, index):
        model = self.comboBoxDefaultSyntax.model()
        node = model.mapToSource(model.createIndex(index, 0))
        self.settingGroup.setValue('defaultSyntax', str(node.internalPointer().uuid).upper())

    def on_editorFlags_toggled(self, checked):
        flags = 0
        for check, flag in self.checks:
            if check.isChecked():
                flags |= flag
        self.settingGroup.setValue('defaultFlags', flags)
