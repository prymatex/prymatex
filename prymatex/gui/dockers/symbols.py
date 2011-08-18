#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 10/02/2010 by defo

from PyQt4 import QtGui
from prymatex.utils.translation import ugettext as _
from prymatex.gui.dockers import PaneDockBase
from prymatex.ui.panesymbols import Ui_SymbolList

class SymbolListWidget(QtGui.QWidget, Ui_SymbolList):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
    
class PMXSymboldListDock(PaneDockBase):
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Symbol List"))
        self.setWidget(SymbolListWidget(self))