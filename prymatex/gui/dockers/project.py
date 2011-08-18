#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 10/02/2010 by defo

from PyQt4.QtGui import *
from prymatex.utils.translation import ugettext as _
from prymatex.gui.dockers import PaneDockBase
from prymatex.ui.paneproject import Ui_ProjectPane

class ProjectWidget(QWidget, Ui_ProjectPane):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)

class PMXProjectDock(PaneDockBase):
    def __init__(self, parent):
        PaneDockBase.__init__(self, parent)
        self.setWidget(ProjectWidget(self))
        