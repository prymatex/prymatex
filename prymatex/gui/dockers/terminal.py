#-*- encoding: utf-8 -*-
import zmq

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.core.plugin.dock import PMXBaseDock
from prymatex.utils.i18n import ugettext as _

PORT = 4613

class PMXTerminalDock(QtGui.QDockWidget, PMXBaseDock):
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea
    MENU_ICON = resources.getIcon("terminal")
    MENU_KEY_SEQUENCE = QtGui.QKeySequence("F4")
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setWindowTitle(_("Terminal"))
        self.setObjectName(_("TerminalDock"))
        self.setupTerminal()
        self.setupSocket()
    
    def setupTerminal(self):
        try:
            from QTermWidget import QTermWidget
            self.terminal = QTermWidget()
            self.terminal.setColorScheme("Linux")
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
        print command
        name = command.get("name")
        args = command.get("args", [])
        kwargs = command.get("kwargs", {})

        method = getattr(self, name)
        method(*args, **kwargs)
        self.sendResult()
        
    def sendResult(self, value = None):
        value = str(value) if value is not None else "ok"
        #Si tengo error retorno en lugar de result un error con { "code": <numero>, "message": "Cadena de error"}
        self.socket.send_pyobj({ "result": value })

    def run(self, command, **kwargs):
        self.terminal.sendText(command)
        
    def setColorScheme(self, schema, **kwargs):
        self.terminal.setColorScheme(schema)