#-*- encoding: utf-8 -*-
import zmq

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.core.plugin.dock import PMXBaseDock
from prymatex.utils.i18n import ugettext as _

PORT = 4613

class PMXTerminalDock(QtGui.QDockWidget, PMXBaseDock):
    SHORTCUT = "F4"
    ICON = resources.getIcon("terminal")
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea

    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setWindowTitle(_("Terminal"))
        self.setObjectName(_("TerminalDock"))
        self.setupTerminal()
        self.setupSocket()
    
    def setMainWindow(self, mainWindow):
        PMXBaseDock.setMainWindow(self, mainWindow)
        mainWindow.terminal = self
        
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
    
    #====================================================
    # ZMQ External actions
    #====================================================
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
        self.sendResult()
        
    def sendResult(self, value = None):
        value = str(value) if value is not None else "ok"
        #Si tengo error retorno en lugar de result un error con { "code": <numero>, "message": "Cadena de error"}
        self.socket.send_pyobj({ "result": value })

    #========================================================
    # Commands
    #========================================================
    def runCommand(self, command):
        if not self.isVisible():
            self.show()
        self.raise_()
        self.terminal.sendText("%s\n" % command)
        
    def chdir(self, directory):
        self.runCommand("cd %s" % directory)
        