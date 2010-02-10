#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 10/02/2010 by defo

from PyQt4.QtGui import *
from prymatex.lib.i18n import ugettext as _


class ProjectWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupGui()
    
    def setupGui(self):
        layout = QVBoxLayout(self)
        self.treeviewProject = QTreeView(self)
        layout.addWidget(self.treeviewProject)
        buttons_layout = QHBoxLayout(self)
        buttons_layout.addWidget(QPushButton(_("New")))
        buttons_layout.addWidget(QPushButton(_("Config")))
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

class PMXProjectDock(QDockWidget):
    def __init__(self, parent):
        QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Project"))
        self.setWidget(ProjectWidget(self))
        