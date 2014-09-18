#!/usr/bin/env python
#-*- encoding: utf-8 -*-
from __future__ import unicode_literals

import os
import signal

from prymatex.utils import osextra

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import create_menu

from prymatex.core import PrymatexDock

from prymatex.utils.i18n import ugettext as _
from prymatex.ui.dockers.process import Ui_ExternalProcessDock

class ExternalProcessDock(PrymatexDock, Ui_ExternalProcessDock, QtWidgets.QDockWidget):
    ICON = "dock-external-process"
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea
    
    def __init__(self, **kwargs):
        super(ExternalProcessDock, self).__init__(**kwargs)
        self.processTableModel = self.application().supportManager.processTableModel
        self.setupUi(self)
        self.tableViewExternalProcess.activated.connect(self.on_tableViewExternalProcess_activated)
        self.tableViewExternalProcess.doubleClicked.connect(self.on_tableViewExternalProcess_doubleClicked)
        self.tableViewExternalProcess.setModel(self.processTableModel)

        #Setup Context Menu
        contextMenu = { 
            "text": "Process",
            "items": [ 
                { "text": "Close",
                  "triggered": self.on_actionCloseProcess_triggered },
                { "text": "Kill",
                  "triggered": self.on_actionKill_triggered },
                { "text": "Terminate",
                  "triggered": self.on_actionTerminate_triggered },
                "-",
                { "text": "Send Signal",
                  "items": [{ "text": "%s (%s)" % (key_value[0], key_value[1]),
                          "triggered": lambda _, signal = key_value[1]: self.on_actionSendSignal_triggered(signal)
                        } for key_value in sorted(iter(osextra.SIGNALS.items()), key = lambda k_v: k_v[1])]
                }
            ]
        }
        self.processMenu = create_menu(self, contextMenu)
        
        self.tableViewExternalProcess.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableViewExternalProcess.customContextMenuRequested.connect(self.showTableViewExternalProcessContextMenu)
        
    def showTableViewExternalProcessContextMenu(self, point):
        index = self.tableViewExternalProcess.indexAt(point)
        if index.isValid():
            self.processMenu.popup(self.tableViewExternalProcess.mapToGlobal(point))
        
    def currentProcess(self):
        index = self.tableViewExternalProcess.currentIndex()
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
        
    def on_tableViewExternalProcess_activated(self, index):
        self.currentProcess().terminate()
    
    def on_tableViewExternalProcess_doubleClicked(self, index):
        self.currentProcess().terminate()
