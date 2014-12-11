#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.core import PrymatexDock

from prymatex.utils.i18n import ugettext as _
from prymatex.gui.codeeditor.editor import CodeEditor
from prymatex.ui.codeeditor.bookmarks import Ui_BookmarksDock
from prymatex.ui.codeeditor.symbols import Ui_SymbolsDock

class CodeEditorSymbolsDock(PrymatexDock, Ui_SymbolsDock, QtWidgets.QDockWidget):
    SHORTCUT = "Ctrl+7"
    ICON = "code-class"
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self, *args, **kwargs):
        super(CodeEditorSymbolsDock, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.tableViewSymbols.activated.connect(self.on_tableViewSymbols_activated)
        self.tableViewSymbols.doubleClicked.connect(self.on_tableViewSymbols_doubleClicked)

    def initialize(self, *args, **kwargs):
        print(*args, **kwargs)
        super(CodeEditorSymbolsDock, self).initialize(*args, **kwargs)
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
        
class CodeEditorBookmarksDock(PrymatexDock, Ui_BookmarksDock, QtWidgets.QDockWidget):
    SHORTCUT = ("Docks", "FileSystemDock", "Alt+M")
    ICON = "bookmarks-organize"
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self, **kwargs):
        super(CodeEditorBookmarksDock, self).__init__(**kwargs)
        self.setupUi(self)
        self.tableViewBookmarks.activated.connect(self.on_tableViewBookmarks_activated)
        self.tableViewBookmarks.doubleClicked.connect(self.on_tableViewBookmarks_doubleClicked)
        
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
