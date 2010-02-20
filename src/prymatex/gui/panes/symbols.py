#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 10/02/2010 by defo

from PyQt4.QtGui import *
from prymatex.lib.i18n import ugettext as _
from prymatex.gui.panes import PaneDockBase
from prymatex.gui.panes.ui_symbols import Ui_SymbolList


class SymbolListWidget(QWidget, Ui_SymbolList):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
    
class PMXSymboldListDock(PaneDockBase):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Symbol List"))
        self.setWidget(SymbolListWidget(self))