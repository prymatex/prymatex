#-*- encoding: utf-8 -*-
import zmq

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.core.plugin.dock import PMXBaseDock
from prymatex.utils.i18n import ugettext as _
import random

PORT = 4613

QTERMWIDGET_IMPORT_SUGGESTOIN = '''
QTermWidget disabled because of:
{}
Please install QTermWidget. Please note QTermWidget consists in a C++ with Python binding.
Get/Update it at https://github.com/D3f0/qtermwidget
'''

class PMXTabTerminals(QtGui.QTabWidget):
    
    def __init__(self, parent = None):
        super(PMXTabTerminals, self).__init__(parent)
        self.addTerminal()
        
    
    def setupUi(self):
        self.pushButtonAddNew = QtGui.QPushButton("+")
        self.pushButtonAddNew.setObjectName("pushButtonAddNew")
        self.setCornerWidget(self.pushButtonAddNew)
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def getTerminal(self):
        ''' Factory '''
        # TODO: Get some initial config?
        from QTermWidget import QTermWidget
        
        return QTermWidget()
    
    def addTerminal(self):
        try:
            term = self.getTerminal()
            term.finished.connect(self.on_terminal_finished)
        #    print(term.availableColorSchemes())
            color = random.choice(term.availableColorSchemes())
            term.setColorScheme(color)
            self.addTab(term, "Shell (color: %s)" % color)
            
        except (ImportError, AttributeError) as exc:
            from traceback import format_exc
            tb = format_exc()
            explainatoryMessage = QtGui.QTextEdit()
            explainatoryMessage.setReadOnly(True)
            explainatoryMessage.setText(_(QTERMWIDGET_IMPORT_SUGGESTOIN).format(tb))
            self.addTab(explainatoryMessage, _("Import Error"))
        
    
    def on_terminal_finished(self):
        terminal = self.sender()
        index = self.indexOf(terminal)
        self.removeTab(index)
        if not self.count():
            self.addTerminal()
    
    @QtCore.pyqtSignature('')
    def on_pushButtonAddNew_pressed(self):
        self.addTerminal()
        
class PMXTerminalDock(QtGui.QDockWidget, PMXBaseDock):
    SHORTCUT = "F4"
    ICON = resources.getIcon("terminal")
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea
    
    terminalAvailable = True
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setWindowTitle(_("Terminal"))
        self.setObjectName(_("TerminalDock"))
        self.setWidget(PMXTabTerminals())
        self.setupSocket()
    
    def initialize(self, mainWindow):
        PMXBaseDock.initialize(self, mainWindow)
        mainWindow.terminal = self
    
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
        
    @property
    def terminal(self):
        return self.widget().currentWidget()
        