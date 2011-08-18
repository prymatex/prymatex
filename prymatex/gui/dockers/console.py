#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4.QtGui import *
from prymatex.core.base import PMXWidget
from prymatex.utils.translation import ugettext as _
from prymatex.gui.dockers import PaneDockBase
from IPython.frontend.qt.console.ipython_widget import IPythonWidget

class PMXConsoleDock(PaneDockBase, PMXWidget):
    def __init__(self, parent):
        PaneDockBase.__init__(self, parent)
        self.setWindowTitle(_("Console"))
        self.console = IPythonWidget()
        self.console.kernel_manager = self.pmxApp.kernelManager
        self.setWidget(self.console)
        