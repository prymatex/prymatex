#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.core.plugin.dock import PMXBaseDock
from prymatex.utils.i18n import ugettext as _

class PMXConsoleDock(QtGui.QDockWidget, PMXBaseDock):
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea
    MENU_KEY_SEQUENCE = QtGui.QKeySequence("F12")
    MENU_ICON = resources.getIcon("console")
    
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setWindowTitle(_("Console"))
        self.setObjectName(_("ConsoleDock"))
        self.setupConsole()

    def setupConsole(self):
        try:
            from IPython.frontend.qt.console.ipython_widget import IPythonWidget
            self.console = IPythonWidget()
            self.console.kernel_manager = self.application.kernelManager
            self.console.set_default_style(colors="linux")
        except ImportError:
            # Gracefuly fail if iPython is not available
            from traceback import format_exc
            self.console = QtGui.QPlainTextEdit()
            self.console.setReadOnly(True)
            tb = format_exc()
            self.console.appendPlainText("IPython console disabled because of\n%s\nPlese install ipython >= 0.11" % tb)
        self.setWidget(self.console)
