#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core import PrymatexDock

from prymatex.utils.i18n import ugettext as _
from prymatex.gui.codeeditor.editor import CodeEditor

class CodeEditorSymbolsDock(PrymatexDock, QtGui.QDockWidget):
    SHORTCUT = "Ctrl+7"
    ICON = "code-class"
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self, **kwargs):
        super(CodeEditorSymbolsDock, self).__init__(**kwargs)
        self.setWindowTitle(_("Symbols"))
        self.setObjectName(_("SymbolsDock"))
        self.tableViewSymbols = QtGui.QTableView()
        self.tableViewSymbols.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableViewSymbols.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewSymbols.setShowGrid(False)
        self.tableViewSymbols.horizontalHeader().setVisible(False)
        self.tableViewSymbols.verticalHeader().setVisible(False)
        self.tableViewSymbols.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableViewSymbols.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableViewSymbols.activated.connect(self.on_tableViewSymbols_activated)
        self.tableViewSymbols.doubleClicked.connect(self.on_tableViewSymbols_doubleClicked)
        self.setWidget(self.tableViewSymbols)

    def initialize(self, **kwargs):
        super(CodeEditorSymbolsDock, self).initialize(**kwargs)
        self.window().currentEditorChanged.connect(self.on_window_currentEditorChanged)

    def on_window_currentEditorChanged(self, editor):
        if isinstance(editor, CodeEditor):
            self.tableViewSymbols.setModel(editor.symbolListModel)
        elif editor is None:
            #Clear
            self.tableViewSymbols.setModel(None)

    def on_tableViewSymbols_activated(self, index):
        block = index.internalPointer()
        self.window().currentEditor().goToBlock(block)
        self.window().currentEditor().setFocus()
    
    def on_tableViewSymbols_doubleClicked(self, index):
        block = index.internalPointer()
        self.window().currentEditor().goToBlock(block)
        self.window().currentEditor().setFocus()
        
class CodeEditorBookmarksDock(PrymatexDock, QtGui.QDockWidget):
    SHORTCUT = ("Docks", "FileSystemDock", "Alt+M")
    ICON = "bookmarks-organize"
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self, **kwargs):
        super(CodeEditorBookmarksDock, self).__init__(**kwargs)
        self.setWindowTitle(_("Bookmarks"))
        self.setObjectName(_("BookmarksDock"))
        self.tableViewBookmarks = QtGui.QTableView()
        self.tableViewBookmarks.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableViewBookmarks.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewBookmarks.setShowGrid(False)
        self.tableViewBookmarks.horizontalHeader().setVisible(False)
        self.tableViewBookmarks.verticalHeader().setVisible(False)
        self.tableViewBookmarks.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableViewBookmarks.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableViewBookmarks.activated.connect(self.on_tableViewBookmarks_activated)
        self.tableViewBookmarks.doubleClicked.connect(self.on_tableViewBookmarks_doubleClicked)
        self.setWidget(self.tableViewBookmarks)
        
    def initialize(self, **kwargs):
        super(CodeEditorBookmarksDock, self).initialize(**kwargs)
        self.window().currentEditorChanged.connect(self.on_window_currentEditorChanged)

    def on_window_currentEditorChanged(self, editor):
        if isinstance(editor, CodeEditor):
            self.tableViewBookmarks.setModel(editor.bookmarkListModel)
        elif editor is None:
            #Clear
            self.tableViewBookmarks.setModel(None)
        
    def on_tableViewBookmarks_activated(self, index):
        cursor = index.internalPointer()
        self.window().currentEditor().setTextCursor(block)
    
    def on_tableViewBookmarks_doubleClicked(self, index):
        cursor = index.internalPointer()
        self.window().currentEditor().setTextCursor(cursor)
