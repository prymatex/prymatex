#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources
from prymatex.ui.configure.editor import Ui_Editor
from prymatex.models.settings import SettingsTreeNode
from prymatex.gui.codeeditor.editor import CodeEditor
from prymatex.gui.codeeditor.sidebar import (LineNumberSideBarAddon, BookmarkSideBarAddon,
                                FoldingSideBarAddon, SelectionSideBarAddon)

class EditorSettingsWidget(SettingsTreeNode, Ui_Editor, QtGui.QWidget):
    TITLE = "Editor"
    ICON = resources.getIcon("accessories-text-editor")

    def __init__(self, **kwargs):
        super(EditorSettingsWidget, self).__init__(nodeName = "editor", **kwargs)
        self.setupUi(self)

        self.checks = [(self.checkBoxWrapLines, CodeEditor.WordWrap),
            (self.checkBoxShowTabSpaces, CodeEditor.ShowTabsAndSpaces),
            (self.checkBoxShowLineParagraph, CodeEditor.ShowLineAndParagraphs),
            (self.checkBoxShowIndentGuide, CodeEditor.IndentGuide),
            (self.checkBoxHighlightCurrenLine, CodeEditor.HighlightCurrentLine),
            (self.checkBoxShowMarginLine, CodeEditor.MarginLine),
        ]

        for check, flag in self.checks:
            check.clicked.connect(self.on_editorFlags_clicked)

        # Get addons groups from profile
        self.bookmarksBarGroup = self.profile.groupByClass(BookmarkSideBarAddon)
        self.lineNumberBarGroup = self.profile.groupByClass(LineNumberSideBarAddon)
        self.foldingBarGroup = self.profile.groupByClass(FoldingSideBarAddon)
        self.selectionBarGroup = self.profile.groupByClass(SelectionSideBarAddon)
	
    def loadSettings(self):
        super(EditorSettingsWidget, self).loadSettings()
        self.comboBoxDefaultSyntax.setModel(self.application.supportManager.syntaxProxyModel)
        self.comboBoxDefaultSyntax.setModelColumn(0)

        uuid = self.settings.value('defaultSyntax')
        syntax = self.application.supportManager.getBundleItem(uuid)
        index = self.comboBoxDefaultSyntax.model().findItemIndex(syntax)
        # TODO Ver porque no esta el valor
        if index:
            self.comboBoxDefaultSyntax.setCurrentIndex(index)

        # Flags
        flags = int(self.settings.value('defaultFlags'))
        for check, flag in self.checks:
            check.setChecked(bool(flags & flag))

        self.spinBoxMarginLineSpace.setValue(self.settings.value("marginLineSize"))

        self.checkBoxLineNumbers.setChecked(self.lineNumberBarGroup.value("showLineNumbers", False))
        self.checkBoxBookmarks.setChecked(self.bookmarksBarGroup.value("showBookmarks", False))
        self.checkBoxFolding.setChecked(self.foldingBarGroup.value("showFolding", False))
        self.checkBoxSelection.setChecked(self.selectionBarGroup.value("showSelection", False))

    def on_checkBoxLineNumbers_clicked(self, checked):
        self.lineNumberBarGroup.setValue('showLineNumbers', self.checkBoxLineNumbers.isChecked())

    def on_checkBoxBookmarks_clicked(self, checked):
        self.bookmarksBarGroup.setValue('showBookmarks', self.checkBoxBookmarks.isChecked())

    def on_checkBoxFolding_clicked(self, checked):
        self.foldingBarGroup.setValue('showFolding', self.checkBoxFolding.isChecked())

    def on_checkBoxSelection_clicked(self, checked):
        self.selectionBarGroup.setValue('showSelection', self.checkBoxSelection.isChecked())

    @QtCore.Slot(int)
    def on_spinBoxMarginLineSpace_valueChanged(self, value):
        self.settings.setValue('marginLineSize', value)

    @QtCore.Slot(int)
    def on_comboBoxDefaultSyntax_activated(self, index):
        model = self.comboBoxDefaultSyntax.model()
        node = model.mapToSource(model.createIndex(index, 0))
        self.settings.setValue('defaultSyntax', str(node.internalPointer().uuid).upper())

    def on_editorFlags_clicked(self, checked):
        flags = 0
        for check, flag in self.checks:
            if check.isChecked():
                flags |= flag
        self.settings.setValue('defaultFlags', flags)
