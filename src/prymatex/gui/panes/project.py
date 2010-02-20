#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 10/02/2010 by defo

from PyQt4.QtGui import *
from prymatex.lib.i18n import ugettext as _
from prymatex.gui.panes import PaneDockBase
from prymatex.gui.panes.ui_project import Ui_ProjectPane

class ProjectWidget(QWidget, Ui_ProjectPane):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
    
    

class PMXProjectDock(PaneDockBase):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Project"))
        self.setWidget(ProjectWidget(self))
        