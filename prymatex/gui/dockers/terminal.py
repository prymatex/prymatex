#-*- encoding: utf-8 -*-
from PyQt4 import QtGui

from prymatex.core.plugin.dock import PMXBaseDock

class PMXTerminalWidget(QtGui.QDockWidget, PMXBaseDock):
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea
    MENU_KEY_SEQUENCE = QtGui.QKeySequence("F4")
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setWindowTitle(_("Terminal"))
        self.setObjectName(_("TerminalDock"))
        self.setupTerminal()

    def setupTerminal(self):
        try:
            from QTermWidget import QTermWidget
            self.terminal = QTermWidget()
            self.terminal.setColorScheme("default")
        except ImportError:
            from traceback import format_exc
            self.terminal = QtGui.QPlainTextEdit()
            self.terminal.setReadOnly(True)
            tb = format_exc()
            self.terminal.appendPlainText("QTermWidget disabled because of\n%s\nPlese install QTermWidget" % tb)
        self.setWidget(self.terminal)