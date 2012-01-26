#-*- encoding: utf-8 -*-
from PyQt4 import QtGui

from prymatex.core.plugin.dock import PMXBaseDock

PORT = 4613

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
    
    def setupSocket(self):
        self.socket = self.application.zmqContext.socket(zmq.REP)
        self.socket.bind('tcp://127.0.0.1:%s' % PORT)
        self.socket.readyRead.connect(self.socketReadyRead)
    
    def socketReadyRead(self):
        command = self.socket.recv_pyobj()
        name = command.get("name")
        args = command.get("args", [])
        kwargs = command.get("kwargs", {})

        method = getattr(self, name)
        method(*args, **kwargs)

     def sendResult(self, value = None):
        value = str(value) if value is not None else "ok"
        #Si tengo error retorno en lugar de result un error con { "code": <numero>, "message": "Cadena de error"}
        self.socket.send_pyobj({ "result": value })
