#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 10/02/2010 by defo

from PyQt4.QtGui import *

class PMXPlistEditWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)


class PMXPlistEditorDock(QDockWidget):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_(""))
        self.setWidget(PMXPlistEditWidget(self))
    