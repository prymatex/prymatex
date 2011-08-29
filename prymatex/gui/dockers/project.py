#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 10/02/2010 by defo

from PyQt4 import QtGui
from prymatex.utils.i18n import ugettext as _
from prymatex.ui.paneproject import Ui_ProjectPane

class ProjectWidget(QtGui.QWidget, Ui_ProjectPane):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

class PMXProjectDock(QtGui.QDockWidget):
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        self.setWidget(ProjectWidget(self))
        