#!/usr/bin/env python
from __future__ import unicode_literals

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.utils import text as textutils

class StatusMixin(object):
    """Docstring for StatusMixin"""

    def initialize(self, *args, **kwargs):
        self.window().editorCreated.connect(self.on_window_editorCreated)
        #self.window().editorChanged.connect(self.on_window_editorChanged)

    def setup(self):
        # Custom Table view for syntax combo
        self.comboBoxSyntaxes.setView(QtWidgets.QTableView(self))
        self.comboBoxSyntaxes.setModel(
            self.application().supportManager.syntaxProxyModel);
        self.comboBoxSyntaxes.setModelColumn(0)
        self.comboBoxSyntaxes.view().resizeColumnsToContents()
        self.comboBoxSyntaxes.view().resizeRowsToContents()
        self.comboBoxSyntaxes.view().verticalHeader().setVisible(False)
        self.comboBoxSyntaxes.view().horizontalHeader().setVisible(False)
        self.comboBoxSyntaxes.view().setShowGrid(False)
        self.comboBoxSyntaxes.view().setMinimumWidth(
            self.comboBoxSyntaxes.view().horizontalHeader().length() + 25)
        self.comboBoxSyntaxes.view().setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.comboBoxSyntaxes.view().setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.comboBoxSyntaxes.view().setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.comboBoxSyntaxes.view().setAutoScroll(False)
        
        # Connect tab size context menu
        self.labelContent.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.labelContent.customContextMenuRequested.connect(self.on_labelContent_customContextMenuRequested)
        
        # Create bundle menu
        self.menuBundle = QtWidgets.QMenu(self)
        self.application().supportManager.appendMenuToBundleMenuGroup(self.menuBundle)
        self.toolButtonMenuBundles.setMenu(self.menuBundle)

    def on_labelContent_customContextMenuRequested(self, point):
        #Setup Context Menu
        menu = QtWidgets.QMenu(self)
        menu.addMenu(self.window().findChild(QtWidgets.QMenu, "menuIndentation"))
        menu.addMenu(self.window().findChild(QtWidgets.QMenu, "menuLineEndings"))
        menu.addMenu(self.window().findChild(QtWidgets.QMenu, "menuEncoding"))
        menu.popup(self.labelContent.mapToGlobal(point))

    def on_window_editorCreated(self, editor):
        editor.cursorPositionChanged.connect(self.on_editor_cursorPositionChanged)
        editor.textChanged.connect(self.on_editor_textChanged)
        editor.syntaxChanged.connect(self.on_editor_syntaxChanged)
        editor.modeChanged.connect(self.on_editor_modeChanged)
    
    @QtCore.Slot(int)
    def on_comboBoxSyntaxes_activated(self, index):
        model = self.comboBoxSyntaxes.model()
        node = model.node(model.createIndex(index, 0))
        self.window().currentEditor().insertBundleItem(node)

    # -------------- Editor signals
    def on_editor_cursorPositionChanged(self):
        editor = self.sender()
        cursor = editor.textCursor()
        self.labelPosition.setText("Line %d, Column %d, Selection %d" % (
            cursor.blockNumber() + 1, cursor.positionInBlock() + 1, 
            cursor.selectionEnd() - cursor.selectionStart()))
        #Set index of current symbol
        #self.comboBoxSymbols.setCurrentIndex(self.comboBoxSymbols.model().findSymbolIndex(cursor))

    def on_editor_textChanged(self):
        editor = self.sender()
        eol = [ eol for eol in textutils.EOLS if eol[0] == editor.eolChars() ]
        self.labelContent.setText("%s %d, Ending %s, Encoding %s" % (
           editor.softTabs() and "Spaces" or "Tab width",
           editor.tabSize(),
           eol and eol[0][2] or "?",
           editor.encoding))
           
    def on_editor_syntaxChanged(self, syntax):
        model = self.comboBoxSyntaxes.model()
        index = model.nodeIndex(syntax).row()
        self.comboBoxSyntaxes.setCurrentIndex(index)

    def on_editor_modeChanged(self):
        editor = self.sender()
        self.labelStatus.setText(editor.currentMode().name())

    def on_window_aboutToEditorChanged(self, editor):
        print(editor)
