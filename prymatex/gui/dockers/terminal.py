#-*- encoding: utf-8 -*-
import zmq
import random
import signal
import os

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.core.settings import pmxConfigPorperty
from prymatex.core.plugin.dock import PMXBaseDock
from prymatex.utils.i18n import ugettext as _

QTERMWIDGET_IMPORT_SUGGESTOIN = '''
QTermWidget disabled because of:
{}
Please install QTermWidget. Please note QTermWidget consists 
in a C++ with Python binding.
Get/Update it at https://github.com/prymatex/qtermwidget
'''

class PMXTabTerminals(QtGui.QTabWidget):
    
    def __init__(self, parent = None):
        super(PMXTabTerminals, self).__init__(parent)
        self.setupCornerWidget()
        self.setupSignals()
        self.setTabsClosable(True)
        #self.setMinimumHeight(200)
    
    def setupSignals(self):    
        self.tabCloseRequested.connect(lambda index, s = self: s.removeTab(index))
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def setupCornerWidget(self):
        widget = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        # Add
        self.pushAddNewTerminal = QtGui.QPushButton()
        self.pushAddNewTerminal.setIcon(resources.getIcon('terminal'))
        self.pushAddNewTerminal.setToolTip(_("Add new terminal"))
        self.pushAddNewTerminal.setFlat(True)

        menuAddNew = QtGui.QMenu()
        actionNew = menuAddNew.addAction("Terminal")
        actionNew.triggered.connect(self.addTerminal)
        actionCustom = menuAddNew.addAction("Run in terminal...")
        actionCustom.triggered.connect(self.launchCustomCommandInTerminal)
        self.pushAddNewTerminal.setMenu(menuAddNew)
        layout.addWidget(self.pushAddNewTerminal)
        
        # Copy
        shortcutCopy = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+c"), self)
        shortcutCopy.activated.connect(lambda s = self: s.currentWidget().copyClipboard())
        
        # Paste
        self.pushPasteIntoTerminal = QtGui.QPushButton()
        self.pushPasteIntoTerminal.setIcon(resources.getIcon('paste'))
        self.pushPasteIntoTerminal.setObjectName('pushPasteIntoTerminal')
        self.pushPasteIntoTerminal.setToolTip('Paste text into terminal')
        self.pushPasteIntoTerminal.setFlat(True)
        self.pushPasteIntoTerminal.pressed.connect(lambda s=self: s.currentWidget().pasteClipboard())
        layout.addWidget(self.pushPasteIntoTerminal)
        
        # Config
        self.pushConfigTerminal = QtGui.QPushButton("C")
        
        #self.pushConfigTerminal.setIcon(getIcon('preference'))
        # self.pushConfigTerminal.setObjectName('pushConfigTerminal')
        # self.pushConfigTerminal.setToolTip('Configure terminal')
        # self.pushConfigTerminal.setFlat(True)
        # layout.addWidget(self.pushConfigTerminal)
        self.cornerMenuButton = QtGui.QPushButton()        
        self.cornerMenuButtonMenu = QtGui.QMenu()
        self.cornerMenuButton.setMenu(self.cornerMenuButtonMenu)
        self.cornerMenuButtonMenu.addAction("Alfa")
        self.cornerMenuButtonMenu.addAction("Beta")
        self.cornerMenuButtonMenu.addAction("Gama")
        
        layout.addWidget(self.cornerMenuButton)
        
        # Close
        self.pushCloseTerminal = QtGui.QPushButton()
        self.pushCloseTerminal.setIcon(resources.getIcon("close"))
        self.pushCloseTerminal.setObjectName("pushCloseTerminal")
        self.pushCloseTerminal.setToolTip(_("Close terminal"))
        self.pushCloseTerminal.setFlat(True)
        
        self.pushCloseTerminal.pressed.connect(lambda s=self: s.removeTab(s.currentIndex()))
        layout.addWidget(self.pushCloseTerminal)
        
        widget.setLayout(layout)
        
        # Save some space
        widget.setStyleSheet('''
        QPushButton {
            margin: 0px;
            padding: 0 0px 0 2px;
        }
        ''')
        self.setCornerWidget(widget)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            print "tecla"
            return False
        return QtGui.QTabWidget.eventFilter(self, obj, event)
     
    def getTerminal(self, cmd = None):
        ''' Factory '''
        from QTermWidget import QTermWidget
        if not cmd:
            term = QTermWidget(1)
        else:
            term = QTermWidget(0)
            term.setShellProgram(cmd)
            term.startShellProgram()
        
        term.setScrollBarPosition(QTermWidget.ScrollBarRight)
        term.finished.connect(self.on_terminal_finished)
        
        term.setColorScheme(self.parent().colorScheme)
        term.setTerminalFont(self.parent().font)
        term.installEventFilter(self)
        return term
    
    def launchCustomCommandInTerminal(self):
        cmd, ok = QtGui.QInputDialog.getText(self, _("Command to run"), _("Command to run"))
        if ok:
            self.addTerminal(cmd)
        
    
    def addTerminal(self, cmd = None, autoFocus = True):
        widget, title = None, "Terminal"
        try:
            widget = self.getTerminal(cmd)
            if not cmd:
                title = "Terminal (PID: %d)" % widget.getShellPID()
            else:
                title = cmd
            
        except (ImportError, AttributeError) as exc:
            from traceback import format_exc
            tb = format_exc()
            widget = QtGui.QTextEdit()
            widget.setReadOnly(True)
            widget.setText(_(QTERMWIDGET_IMPORT_SUGGESTOIN).format(tb))
            title = _("Import Error")
        self.addTab(widget, title)
        if autoFocus:
            self.setCurrentWidget(widget)
            widget.setFocus()
        

    #===========================================================================
    # Mouse events
    #===========================================================================
    def mouseDoubleClickEvent(self, event):
        self.addTerminal()
    
    def clickedItem(self, pos):
        for i in range(self.tabBar().count()):
            if self.tabBar().tabRect(i).contains(pos):
                return self.widget(i)
    #===========================================================================
    # Context menu stuff
    #===========================================================================
    def mousePressEvent(self, event):
        from QTermWidget import QTermWidget
        if event.button() == QtCore.Qt.RightButton:
            menu = QtGui.QMenu()
            widget = self.clickedItem(event.pos())
            if not widget:
                actionAddTerm = menu.addAction(_('Add terminal'))
                actionAddTerm.triggered.connect(self.addTerminal)
                
            else:
                pid = widget.getShellPID()
                # Close
                closeAction = menu.addAction(_("Close"))
                closeAction.triggered.connect(lambda index, s=self: s.removeTab(index))
                menu.addSeparator()
                # Signals
                signalSubMenu = menu.addMenu(_("&Send signal"))
                for name, number in SIGNALS:
                    signal = signalSubMenu.addAction("Send %s (%d)" % (name, number))
                    signal.triggered.connect(lambda pid = pid, number = number: os.kill(pid, number))
                # Scrollbar
                scrollBarMenu = QtGui.QMenu("Scrollbar")
                for name, enumVal in (("No Scrollbar", QTermWidget.NoScrollBar),
                                      ("Left Scrollbar",QTermWidget.ScrollBarLeft),
                                      ("Right Scrollbar", QTermWidget.ScrollBarRight)):
                    action = scrollBarMenu.addAction(name)
                    action.triggered.connect(lambda w=widget, n=enumVal: widget.setScrollBarPosition(n))
                menu.addMenu(scrollBarMenu)
                
                # Colors
                menuColors = QtGui.QMenu("Color Scheme")
                for name in widget.availableColorSchemes():
                    action = menuColors.addAction(name)
                    action.triggered.connect(lambda w=widget, n=name: widget.setColorScheme(n))
                
                menu.addMenu(menuColors)
                
            menu.exec_(event.globalPos())
            return
        super(PMXTabTerminals, self).mousePressEvent(event)
    
    def buildSingalMenu(self, process_pid):
        '''Creates a singal with add hock menu events'''
        menu = QtGui.QMenu(_('Send &Singal'))
        # Signals
        
        
    def sendSignalToCurrentProcess(self):
        pass
    
    
    def quitTab(self, index = None):
        if index is None:
            index = self.currentIndex()
        terminal = self.widget(index)
        self.removeTab(terminal)
    
    def on_terminal_finished(self):
        terminal = self.sender()
        index = self.indexOf(terminal)
        self.removeTab(index)
        
    def tabRemoved(self, index):
        # Do not allow the tab widget be empty
        if not self.count():
            self.addTerminal()
    
class PMXTerminalDock(QtGui.QDockWidget, PMXBaseDock):
    SHORTCUT = "F4"
    ICON = resources.getIcon("terminal")
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea
    
    #=======================================================================
    # Settings
    #=======================================================================
    SETTINGS_GROUP = 'Terminal'

    @pmxConfigPorperty(default = "linux")
    def colorScheme(self, scheme):
        for index in range(self.tabTerminals.count()):
            self.tabTerminals.widget(index).setColorScheme(scheme)
    
    @pmxConfigPorperty(default = QtGui.QFont("Monospace", 9))
    def font(self, font):
        for index in range(self.tabTerminals.count()):
            self.tabTerminals.widget(index).setTerminalFont(font)

    terminalAvailable = True
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setWindowTitle(_("Terminal"))
        self.setObjectName(_("TerminalDock"))
        self.tabTerminals = PMXTabTerminals(self)
        self.setWidget(self.tabTerminals)
        self.setupSocket()
        self.installEventFilter(self)
    
    
    def initialize(self, mainWindow):
        PMXBaseDock.initialize(self, mainWindow)
        mainWindow.terminal = self
        self.widget().addTerminal()
    
    def eventFilter(self, obj, event):
        if obj == self and event.type() == QtCore.QEvent.KeyPress:
            if event.modifiers() == QtCore.Qt.ControlModifier and event.key() in [ QtCore.Qt.Key_W]:
                print "W"
                return
        return super(PMXTerminalDock, self).eventFilter(obj, event)
    
    #====================================================
    # ZMQ External actions
    #====================================================
    def setupSocket(self):
        self.socket = self.application.zmqSocket(zmq.REP, "Terminal")
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
        self.terminal.sendText("\r%s\n" % command)
        
    def chdir(self, directory):
        self.runCommand('cd "%s"' % directory)
        
    @property
    def terminal(self):
        return self.widget().currentWidget()
    
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.terminal import PMXTerminalSettings
        return [ PMXTerminalSettings ]
    
    
    
    def showEvent(self, event):
        self.widget().setFocus()
        
#===============================================================================
# Signals
#===============================================================================
SIGNALS = [ ("%s" % x, getattr(signal, x)) for x in dir(signal) if x.startswith('SIG')]
def signame_by_id(n):
    try:
        return [ name for name, number in SIGNALS if number == n ][0]
    except:
        return _("Uknown signal")
    
def sendSignalToProcess(pid, sig):
    print("Sending %s to %s" % (signame_by_id(sig), pid))
    os.kill(pid, sig)
    
    
