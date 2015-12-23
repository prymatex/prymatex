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

    def setStatus(self, message):
        self.labelMessage.setText(message)

    # -------------- Content tool
    def _update_content(self, editor):
        eol = [ eol for eol in textutils.EOLS if eol[0] == editor.eolChars() ]
        self.labelContent.setText("%s %d, Ending %s, Encoding %s" % (
            editor.softTabs() and "Spaces" or "Tab width",
            editor.tabSize(),
            eol and eol[0][2] or "?",
            editor.encoding)
        )
    
    # -------------- Syntax tool
    def _update_syntax(self, editor):
        model = self.comboBoxSyntaxes.model()
        node = model.findNode(QtCore.Qt.UUIDRole, editor.syntax().uuidAsText())
        index = model.indexFromNode(node)
        self.comboBoxSyntaxes.setCurrentIndex(index.row())
        
    def on_labelContent_customContextMenuRequested(self, point):
        #Setup Context Menu
        menu = QtWidgets.QMenu(self)
        menu.addMenu(self.window().findChild(QtWidgets.QMenu, "menuTabSize"))
        menu.addMenu(self.window().findChild(QtWidgets.QMenu, "menuLineEndings"))
        menu.addMenu(self.window().findChild(QtWidgets.QMenu, "menuEncoding"))
        menu.popup(self.labelContent.mapToGlobal(point))

    # -------------- Window signals
    def on_window_editorCreated(self, editor):
        editor.textChanged.connect(self.on_editor_textChanged)
        editor.syntaxChanged.connect(self.on_editor_syntaxChanged)
    
    def on_window_editorChanged(self, editor):
        self._update_content(editor)
        self._update_syntax(editor)

    def on_window_aboutToEditorChange(self, editor):
        pass

    def on_window_aboutToEditorDelete(self, editor):
        editor.textChanged.disconnect(self.on_editor_textChanged)
        editor.syntaxChanged.disconnect(self.on_editor_syntaxChanged)

    @QtCore.Slot(int)
    def on_comboBoxSyntaxes_activated(self, index):
        model = self.comboBoxSyntaxes.model()
        node = model.node(model.index(index))
        self.window().currentEditor().insertBundleItem(node.bundleItem())

    # -------------- Editor signals
    @QtCore.Slot()
    def on_editor_textChanged(self):
        self._update_content(self.sender())
    
    @QtCore.Slot(object)    
    def on_editor_syntaxChanged(self, syntax):
        self._update_syntax(self.sender())
