#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui
from prymatex.utils.i18n import ugettext as _

class PMXCodeSymbolsDock(QtGui.QDockWidget):
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Symbols"))
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
        
    def setCurrentEditor(self, editor):
        self.currentEditor = editor
        if editor is not None:
            self.tableViewSymbols.setModel(editor.symbols)
        
    def on_tableViewSymbols_activated(self, index):
        block = index.internalPointer()
        self.currentEditor.goToBlock(block)
    
    def on_tableViewSymbols_doubleClicked(self, index):
        block = index.internalPointer()
        self.currentEditor.goToBlock(block)
        
class PMXCodeBookmarksDock(QtGui.QDockWidget):
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Bookmarks"))
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
        
    def setCurrentEditor(self, editor):
        self.currentEditor = editor
        if editor is not None:
            self.tableViewBookmarks.setModel(editor.bookmarks)
        
    def on_tableViewBookmarks_activated(self, index):
        block = index.internalPointer()
        self.currentEditor.goToBlock(block)
    
    def on_tableViewBookmarks_doubleClicked(self, index):
        block = index.internalPointer()
        self.currentEditor.goToBlock(block)