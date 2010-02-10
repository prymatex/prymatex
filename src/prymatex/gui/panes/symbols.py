#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 10/02/2010 by defo

from PyQt4.QtGui import *
from prymatex.lib.i18n import ugettext as _


class SymbolListWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupGui()
    
    def setupGui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QTreeView(self))
        layout_buttons = QHBoxLayout(self)
        layout_buttons.addWidget(QPushButton(_("Refresh")))
        layout_buttons.addStretch(-1)
        self.setLayout(layout)
        
class PMXSymboldListDock(QDockWidget):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Symbol List"))
        self.setWidget(SymbolListWidget(self))