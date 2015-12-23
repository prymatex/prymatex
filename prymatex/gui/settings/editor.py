#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.ui.configure.editor import Ui_Editor
from prymatex.models.settings import SettingsTreeNode
from prymatex.gui.codeeditor.editor import CodeEditor
from prymatex.gui.codeeditor.sidebar import (LineNumberSideBarAddon, 
    BookmarkSideBarAddon, FoldingSideBarAddon, SelectionSideBarAddon)

class EditorSettingsWidget(SettingsTreeNode, Ui_Editor, QtWidgets.QWidget):
    def __init__(self, component_class, **kwargs):
        super(EditorSettingsWidget, self).__init__(component_class, nodeName="editor", **kwargs)
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
	
    def loadSettings(self):
        super(EditorSettingsWidget, self).loadSettings()
        self.setTitle("Editor")
        self.setIcon(self.application().resources().get_icon("settings-editor"))

        # Get addons groups from profile
        self.bookmarksBarGroup = self.application().settingsManager.settingsForClass(BookmarkSideBarAddon)
        self.lineNumberBarGroup = self.application().settingsManager.settingsForClass(LineNumberSideBarAddon)
        self.foldingBarGroup = self.application().settingsManager.settingsForClass(FoldingSideBarAddon)
        self.selectionBarGroup = self.application().settingsManager.settingsForClass(SelectionSideBarAddon)

        self.comboBoxDefaultSyntax.setModel(self.application().supportManager.syntaxProxyModel)
        self.comboBoxDefaultSyntax.setModelColumn(0)

        syntax_uuid = self.settings().get('default_syntax')
        if syntax_uuid is not None:
            node = self.application().supportManager.getManagedObjectNode(syntax_uuid)
            index = self.comboBoxDefaultSyntax.model().indexFromNode(node)
            self.comboBoxDefaultSyntax.setCurrentIndex(index.row())

        # Flags
        flags = int(self.settings().get('default_flags'))
        for check, flag in self.checks:
            check.setChecked(bool(flags & flag))

        self.spinBoxMarginLineSpace.setValue(self.settings().get("margin_line_size"))

        self.checkBoxLineNumbers.setChecked(self.lineNumberBarGroup.get("show_line_numbers", False))
        self.checkBoxBookmarks.setChecked(self.bookmarksBarGroup.get("show_bookmarks", False))
        self.checkBoxFolding.setChecked(self.foldingBarGroup.get("show_folding", False))
        self.checkBoxSelection.setChecked(self.selectionBarGroup.get("show_selection", False))

    @QtCore.Slot(bool)
    def on_checkBoxLineNumbers_clicked(self, checked):
        self.lineNumberBarGroup.set('show_line_numbers', self.checkBoxLineNumbers.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxBookmarks_clicked(self, checked):
        self.bookmarksBarGroup.set('show_bookmarks', self.checkBoxBookmarks.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxFolding_clicked(self, checked):
        self.foldingBarGroup.set('show_folding', self.checkBoxFolding.isChecked())

    @QtCore.Slot(bool)
    def on_checkBoxSelection_clicked(self, checked):
        self.selectionBarGroup.set('show_selection', self.checkBoxSelection.isChecked())

    @QtCore.Slot(int)
    def on_spinBoxMarginLineSpace_valueChanged(self, value):
        self.settings().set('margin_line_size', value)

    @QtCore.Slot(int)
    def on_comboBoxDefaultSyntax_activated(self, index):
        model = self.comboBoxDefaultSyntax.model()
        index = model.mapToSource(model.createIndex(index, 0))
        self.settings().set('default_syntax', str(index.internalPointer().uuid).upper())

    def on_editorFlags_clicked(self, checked):
        flags = 0
        for check, flag in self.checks:
            if check.isChecked():
                flags |= flag
        self.settings().set('default_flags', flags)

