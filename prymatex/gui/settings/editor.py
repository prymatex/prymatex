#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.ui.configure.editor import Ui_Editor
from prymatex.models.settings import SettingsTreeNode
from prymatex.gui.codeeditor.editor import CodeEditor
from prymatex.gui.codeeditor.sidebar import (LineNumberSideBarAddon, 
    BookmarkSideBarAddon, FoldingSideBarAddon, SelectionSideBarAddon)

class EditorSettingsWidget(SettingsTreeNode, Ui_Editor, QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super(EditorSettingsWidget, self).__init__(nodeName = "editor", **kwargs)
        self.setupUi(self)
        self.setTitle("Editor")
        self.setIcon(self.resources().get_icon("settings-editor"))

        self.checks = [(self.checkBoxWrapLines, CodeEditor.WordWrap),
            (self.checkBoxShowTabSpaces, CodeEditor.ShowTabsAndSpaces),
            (self.checkBoxShowLineParagraph, CodeEditor.ShowLineAndParagraphs),
            (self.checkBoxShowIndentGuide, CodeEditor.IndentGuide),
            (self.checkBoxHighlightCurrenLine, CodeEditor.HighlightCurrentLine),
            (self.checkBoxShowMarginLine, CodeEditor.MarginLine),
        ]

        for check, flag in self.checks:
            check.clicked.connect(self.on_editorFlags_clicked)
	
    def loadSettings(self):
        super(EditorSettingsWidget, self).loadSettings()

        # Get addons groups from profile
        self.bookmarksBarGroup = self.application().settingsManager.settingsForClass(BookmarkSideBarAddon)
        self.lineNumberBarGroup = self.application().settingsManager.settingsForClass(LineNumberSideBarAddon)
        self.foldingBarGroup = self.application().settingsManager.settingsForClass(FoldingSideBarAddon)
        self.selectionBarGroup = self.application().settingsManager.settingsForClass(SelectionSideBarAddon)

        self.comboBoxDefaultSyntax.setModel(self.application().supportManager.syntaxProxyModel)
        self.comboBoxDefaultSyntax.setModelColumn(0)

        uuid = self.settings.get('defaultSyntax')
        syntax = self.application().supportManager.getBundleItem(uuid)
        index = self.comboBoxDefaultSyntax.model().nodeIndex(syntax).row()
        # TODO Ver porque no esta el valor
        if index:
            self.comboBoxDefaultSyntax.setCurrentIndex(index)

        # Flags
        flags = int(self.settings.get('defaultFlags'))
        for check, flag in self.checks:
            check.setChecked(bool(flags & flag))

        self.spinBoxMarginLineSpace.setValue(self.settings.get("marginLineSize"))

        self.checkBoxLineNumbers.setChecked(self.lineNumberBarGroup.get("showLineNumbers", False))
        self.checkBoxBookmarks.setChecked(self.bookmarksBarGroup.get("showBookmarks", False))
        self.checkBoxFolding.setChecked(self.foldingBarGroup.get("showFolding", False))
        self.checkBoxSelection.setChecked(self.selectionBarGroup.get("showSelection", False))

    @QtCore.Slot(bool)
    def on_checkBoxLineNumbers_clicked(self, checked):
        self.lineNumberBarGroup.set('showLineNumbers', self.checkBoxLineNumbers.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxBookmarks_clicked(self, checked):
        self.bookmarksBarGroup.set('showBookmarks', self.checkBoxBookmarks.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxFolding_clicked(self, checked):
        self.foldingBarGroup.set('showFolding', self.checkBoxFolding.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxSelection_clicked(self, checked):
        self.selectionBarGroup.set('showSelection', self.checkBoxSelection.isChecked())

    @QtCore.Slot(int)
    def on_spinBoxMarginLineSpace_valueChanged(self, value):
        self.settings.set('marginLineSize', value)

    @QtCore.Slot(int)
    def on_comboBoxDefaultSyntax_activated(self, index):
        model = self.comboBoxDefaultSyntax.model()
        node = model.mapToSource(model.createIndex(index, 0))
        self.settings.set('defaultSyntax', str(node.internalPointer().uuid).upper())

    def on_editorFlags_clicked(self, checked):
        flags = 0
        for check, flag in self.checks:
            if check.isChecked():
                flags |= flag
        self.settings.set('defaultFlags', flags)
