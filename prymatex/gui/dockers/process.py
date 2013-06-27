#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import signal

from prymatex.utils import osextra

from prymatex.qt import QtGui, QtCore
from prymatex.qt.helpers import create_menu

from prymatex.core import PMXBaseDock

from prymatex import resources
from prymatex.utils.i18n import ugettext as _

class PMXProcessDock(QtGui.QDockWidget, PMXBaseDock):
    SHORTCUT = "F7"
    ICON = resources.getIcon("application-x-executable-script")
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("External process"))
        self.setObjectName(_("ExternalProcessDock"))
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
            "text": "Process",
            "items": [ 
                { "text": "Close",
                  "callback": self.on_actionCloseProcess_triggered },
                { "text": "Kill",
                  "callback": self.on_actionKill_triggered },
                { "text": "Terminate",
                  "callback": self.on_actionTerminate_triggered },
                "-",
                { "text": "Send Signal",
                  "items": [{ "text": "%s (%s)" % (key_value[0], key_value[1]),
                          "callback": lambda _, signal = key_value[1]: self.on_actionSendSignal_triggered(signal)
                        } for key_value in sorted(iter(osextra.SIGNALS.items()), key = lambda k_v: k_v[1])]
                }
            ]
        }
        self.processMenu, self.processMenuActions = create_menu(self, contextMenu)

        for action in self.processMenuActions:
            if hasattr(action, "callback"):
                action.triggered.connect(action.callback)
        
        self.tableViewProcess.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableViewProcess.customContextMenuRequested.connect(self.showtableViewProcessContextMenu)
        
    def showtableViewProcessContextMenu(self, point):
        index = self.tableViewProcess.indexAt(point)
        if index.isValid():
            self.processMenu.popup(self.tableViewProcess.mapToGlobal(point))
        
    def currentProcess(self):
        index = self.tableViewProcess.currentIndex()
        return self.processTableModel.processForIndex(index)

    def on_actionCloseProcess_triggered(self):
        """docstring for on_actionCloseProcess_triggered"""
        self.currentProcess().close()
    
    def on_actionKill_triggered(self):
        self.currentProcess().kill()
        
    def on_actionSendSignal_triggered(self, signal):
        os.kill(self.currentProcess().pid(), signal)
        
    def on_actionTerminate_triggered(self):
        self.currentProcess().terminate()
        
    def on_tableViewProcess_activated(self, index):
        self.currentProcess().terminate()
    
    def on_tableViewProcess_doubleClicked(self, index):
        self.currentProcess().terminate()