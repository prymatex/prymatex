#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.utils.i18n import ugettext as _
from prymatex.core.plugin.dock import PMXBaseDock

class PMXProcessDock(QtGui.QDockWidget, PMXBaseDock):
    SHORTCUT = "F7"
    ICON = resources.getIcon("symbols")
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Process"))
        self.setObjectName(_("ProcessDock"))
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
        self.tableViewSymbols.setModel(self.application.supportManager.processListModel)
        self.setWidget(self.tableViewSymbols)

    def on_tableViewSymbols_activated(self, index):
        print index
    
    def on_tableViewSymbols_doubleClicked(self, index):
        print index
