#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 08/02/2010 by defo

from PyQt4.QtGui import QDockWidget, QWidget, QVBoxLayout, QHBoxLayout

from PyQt4.QtGui import QPushButton, QTextEdit



class PMXTracebackConsoleWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.stupGui()
        
    def setupGui(self):
        layout = QVBoxLayout(self)
        self.textEdit = QTextEdit(self)
        
        
        layout.addWidget(self.textEdit)
        
        self.setLayout(layout)
        
        

class PMXTracebackConsoleDock(QDockWidget):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Traceback Console"))
        self.setWidget(PMXTracebackConsoleWidget(self))