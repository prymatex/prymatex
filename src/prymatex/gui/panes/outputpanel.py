#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 10/02/2010 by defo
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from prymatex.utils.i18n import ugettext as _
from prymatex.gui.panes import PaneDockBase

class OutputPanel(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupGui()
    
    def setupGui(self):
        layout = QVBoxLayout(self)
        self.texteditOutput = QTextEdit(self)
        #self.texteditOutput.setEd
        #self.texteditOutput.setH
        layout.addWidget(self.texteditOutput)
        
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(QPushButton(_("Clear")))
        layout_buttons.addStretch(-1)
        layout.addLayout(layout_buttons)
        self.setLayout(layout)

class PMXOutputDock(PaneDockBase):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Output"))
        self.setWidget(OutputPanel(self))
        