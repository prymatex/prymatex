#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui
from prymatex.core.base import PMXObject
from prymatex.utils.i18n import ugettext as _
try:
    from IPython.frontend.qt.console.ipython_widget import IPythonWidget
    IPYTHON_QT_AVAILABLE = True
except ImportError:
    IPYTHON_QT_AVAILABLE = False


class PMXConsoleDock(QtGui.QDockWidget, PMXObject):
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        self.setWindowTitle(_("Console"))
        
        try:
           assert IPYTHON_QT_AVAILABLE, "Plese install ipython >= 0.11"
           self.console = IPythonWidget()
           self.console.kernel_manager = self.application.kernelManager
        except Exception:
            # Gracefuly fail if iPython is not available
            from traceback import format_exc
            self.console = QtGui.QPlainTextEdit()
            self.console.setReadOnly(True)
            tb = format_exc()
            self.console.appendPlainText("IPython console disabled because of\n%s" % tb)
        self.setWidget(self.console)
        
