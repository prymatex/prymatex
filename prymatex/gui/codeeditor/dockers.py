#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core import PMXBaseDock

from prymatex import resources
from prymatex.utils.i18n import ugettext as _
from prymatex.gui.codeeditor.editor import CodeEditor

class CodeEditorSymbolsDock(QtGui.QDockWidget, PMXBaseDock):
    SHORTCUT = "Ctrl+7"
    ICON = resources.getIcon("code-class")
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Symbols"))
        self.setObjectName(_("SymbolsDock"))
        PMXBaseDock.__init__(self)
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

    def initialize(self, mainWindow):
        PMXBaseDock.initialize(self, mainWindow)
        mainWindow.currentEditorChanged.connect(self.on_mainWindow_currentEditorChanged)

    def on_mainWindow_currentEditorChanged(self, editor):
        if isinstance(editor, CodeEditor):
            self.tableViewSymbols.setModel(editor.symbolListModel)
        elif editor is None:
            #Clear
            self.tableViewSymbols.setModel(None)

    def on_tableViewSymbols_activated(self, index):
        block = index.internalPointer()
        self.mainWindow.currentEditor().goToBlock(block)
        self.mainWindow.currentEditor().setFocus()
    
    def on_tableViewSymbols_doubleClicked(self, index):
        block = index.internalPointer()
        self.mainWindow.currentEditor().goToBlock(block)
        self.mainWindow.currentEditor().setFocus()
        
class CodeEditorBookmarksDock(QtGui.QDockWidget, PMXBaseDock):
    SHORTCUT = resources.get_sequence("Docks", "FileSystemDock", "Alt+M")
    ICON = resources.getIcon("bookmarks-organize")
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self, mainWindow):
        QtGui.QDockWidget.__init__(self, mainWindow)
        PMXBaseDock.__init__(self)
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
        
    def initialize(self, mainWindow):
        PMXBaseDock.initialize(self, mainWindow)
        mainWindow.currentEditorChanged.connect(self.on_mainWindow_currentEditorChanged)

    def on_mainWindow_currentEditorChanged(self, editor):
        if isinstance(editor, CodeEditor):
            self.tableViewBookmarks.setModel(editor.bookmarkListModel)
        elif editor is None:
            #Clear
            self.tableViewBookmarks.setModel(None)
        
    def on_tableViewBookmarks_activated(self, index):
        cursor = index.internalPointer()
        self.mainWindow.currentEditor().setTextCursor(block)
    
    def on_tableViewBookmarks_doubleClicked(self, index):
        cursor = index.internalPointer()
        self.mainWindow.currentEditor().setTextCursor(cursor)
