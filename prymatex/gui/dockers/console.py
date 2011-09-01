#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui
from prymatex.core.base import PMXObject
from prymatex.utils.i18n import ugettext as _
from IPython.frontend.qt.console.ipython_widget import IPythonWidget

class PMXConsoleDock(QtGui.QDockWidget, PMXObject):
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Console"))
        self.console = IPythonWidget()
        self.console.kernel_manager = self.application.kernelManager
        self.setWidget(self.console)
        