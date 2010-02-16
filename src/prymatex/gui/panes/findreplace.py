#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 10/02/2010 by defo

from PyQt4.QtGui import *
from prymatex.gui.panes import PaneDockBase

class PMXFindReplaceDockWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        
    def setupGui(self):
        layout = QFormLayout(self)
        
        self.setLayout(layout)
        
class PMXFindReplaceDock(PaneDockBase):
    def __init__(self, parent):
        QDockWidget.__init__(self)
        # TODO: Set allowed areas
        #self.setAllowedAreas(QDockWidget.)
        #self.setWin
        self.setWidget(PMXFindReplaceDockWidget(self))
    