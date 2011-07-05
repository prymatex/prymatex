#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui
from prymatex.gui.panes import PaneDockBase
from prymatex.utils.translation import ugettext as _

class PMXTracebackConsoleWidget(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.stupGui()
        
    def setupGui(self):
        layout = QtGui.QVBoxLayout(self)
        self.textEdit = QtGui.QTextEdit(self)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

class PMXTracebackConsoleDock(PaneDockBase):
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Traceback Console"))
        self.setWidget(PMXTracebackConsoleWidget(self))