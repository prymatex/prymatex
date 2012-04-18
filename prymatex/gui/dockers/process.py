#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.utils.i18n import ugettext as _
from prymatex.gui import utils
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
        self.processTableModel = self.application.supportManager.processTableModel
        self.tableViewProcess = QtGui.QTableView()
        self.tableViewProcess.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableViewProcess.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewProcess.setShowGrid(False)
        self.tableViewProcess.horizontalHeader().setVisible(False)
        self.tableViewProcess.verticalHeader().setVisible(False)
        self.tableViewProcess.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableViewProcess.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tableViewProcess.activated.connect(self.on_tableViewProcess_activated)
        self.tableViewProcess.doubleClicked.connect(self.on_tableViewProcess_doubleClicked)
        self.tableViewProcess.setModel(self.processTableModel)
        self.setWidget(self.tableViewProcess)

        #Setup Context Menu
        contextMenu = { 
            "title": "Process",
            "items": [ { "title": "Kill"}, {"title": "Terminate"} ]
        }
        self.processMenu, self.processMenuActions = utils.createQMenu(contextMenu, self)

        self.processMenuActions[0].triggered.connect(self.on_actionKill_triggered)
        self.processMenuActions[1].triggered.connect(self.on_actionTerminate_triggered)
                
        self.tableViewProcess.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableViewProcess.customContextMenuRequested.connect(self.showtableViewProcessContextMenu)
        
    def showtableViewProcessContextMenu(self, point):
        index = self.tableViewProcess.indexAt(point)
        if index.isValid():
            self.processMenu.popup(self.tableViewProcess.mapToGlobal(point))
        
    def currentProcess(self):
        index = self.tableViewProcess.currentIndex()
        return self.processTableModel.processForIndex(index)

    def on_actionKill_triggered(self):
        self.currentProcess().kill()
        
    def on_actionTerminate_triggered(self):
        self.currentProcess().terminate()
        
    def on_tableViewProcess_activated(self, index):
        self.currentProcess().terminate()
    
    def on_tableViewProcess_doubleClicked(self, index):
        self.currentProcess().terminate()
