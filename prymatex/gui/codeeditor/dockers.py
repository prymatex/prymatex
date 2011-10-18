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
        self.setWidget(self.tableViewSymbols)
        
    def setCurrentEditor(self, editor):
        self.tableViewSymbols.setModel(editor.symbols)