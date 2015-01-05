#!/usr/bin/env python
from __future__ import unicode_literals

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.utils import text as textutils

class StatusMixin(object):
    """Docstring for StatusMixin"""

    def initialize(self, *args, **kwargs):
        self.window().editorCreated.connect(self.on_window_editorCreated)
        self.window().editorChanged.connect(self.on_window_editorChanged)
        self.window().aboutToEditorChange.connect(self.on_window_aboutToEditorChange)
        self.window().aboutToEditorDelete.connect(self.on_window_aboutToEditorDelete)
        
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

    # -------------- Position tool
    def _update_position(self, editor):
        cursor = editor.textCursor()
        self.labelPosition.setText("Line %d, Column %d, Selection %d" % (
            cursor.blockNumber() + 1, cursor.positionInBlock() + 1, 
            cursor.selectionEnd() - cursor.selectionStart())
        )
        self.comboBoxSymbols.setCurrentIndex(self.comboBoxSymbols.model().findSymbolIndex(cursor))

    # -------------- Content tool
    def _update_content(self, editor):
        eol = [ eol for eol in textutils.EOLS if eol[0] == editor.eolChars() ]
        self.labelContent.setText("%s %d, Ending %s, Encoding %s" % (
            editor.softTabs() and "Spaces" or "Tab width",
            editor.tabSize(),
            eol and eol[0][2] or "?",
            editor.encoding)
        )
    
    # -------------- Mode tool
    def _update_mode(self, editor):
        self.labelStatus.setText(editor.currentMode().name())
    
    # -------------- Syntax tool
    def _update_mode(self, editor):
        self.labelStatus.setText(editor.currentMode().name())

    def _update_syntax(self, editor):
        model = self.comboBoxSyntaxes.model()
        index = model.nodeIndex(editor.syntax()).row()
        self.comboBoxSyntaxes.setCurrentIndex(index)
        
    def on_labelContent_customContextMenuRequested(self, point):
        #Setup Context Menu
        menu = QtWidgets.QMenu(self)
        menu.addMenu(self.window().findChild(QtWidgets.QMenu, "menuIndentation"))
        menu.addMenu(self.window().findChild(QtWidgets.QMenu, "menuLineEndings"))
        menu.addMenu(self.window().findChild(QtWidgets.QMenu, "menuEncoding"))
        menu.popup(self.labelContent.mapToGlobal(point))

    # -------------- Window signals
    def on_window_editorCreated(self, editor):
        editor.cursorPositionChanged.connect(self.on_editor_cursorPositionChanged)
        editor.textChanged.connect(self.on_editor_textChanged)
        editor.syntaxChanged.connect(self.on_editor_syntaxChanged)
        editor.modeChanged.connect(self.on_editor_modeChanged)
    
    def on_window_editorChanged(self, editor):
        self.comboBoxSymbols.setModel(editor.symbolListModel)
        self._update_position(editor)
        self._update_content(editor)
        self._update_mode(editor)
        self._update_syntax(editor)

    def on_window_aboutToEditorChange(self, editor):
        print("About to change", editor)

    def on_window_aboutToEditorDelete(self, editor):
        editor.cursorPositionChanged.disconnect(self.on_editor_cursorPositionChanged)
        editor.textChanged.disconnect(self.on_editor_textChanged)
        editor.syntaxChanged.disconnect(self.on_editor_syntaxChanged)
        editor.modeChanged.disconnect(self.on_editor_modeChanged)

    @QtCore.Slot(int)
    def on_comboBoxSyntaxes_activated(self, index):
        model = self.comboBoxSyntaxes.model()
        node = model.node(model.index(index))
        self.window().currentEditor().insertBundleItem(node)

    @QtCore.Slot(int)
    def on_comboBoxSymbols_activated(self, index):
        model = self.comboBoxSymbols.model()
        cursor = model.symbolCursor(model.index(index))
        if not cursor.isNull():
            self.window().currentEditor().setTextCursor(cursor)

    # -------------- Editor signals
    def on_editor_cursorPositionChanged(self):
        self._update_position(self.sender())

    def on_editor_textChanged(self):
        self._update_content(self.sender())
        
    def on_editor_syntaxChanged(self, syntax):
        self._update_syntax(self.sender())

    def on_editor_modeChanged(self):
        self._update_mode(self.sender())

