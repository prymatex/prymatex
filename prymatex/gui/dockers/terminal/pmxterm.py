#-*- encoding: utf-8 -*-

import os, sys

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseDock

from prymatex import resources
from prymatex.core.settings import pmxConfigPorperty
from prymatex.utils.i18n import ugettext as _
from prymatex.utils.programs import python_script_exists
from prymatex.widgets.pmxterm import Session, TerminalWidget, ProcessInfo


class TabbedTerminal(QtGui.QTabWidget):

    
    def __init__(self, parent=None):
        super(TabbedTerminal, self).__init__(parent)
        self.proc_info = ProcessInfo()
        self.setTabPosition(QtGui.QTabWidget.South)
        self._new_button = QtGui.QPushButton(self)
        self._new_button.setText("New")
        self._new_button.clicked.connect(self.newTerminal)
        self.setCornerWidget(self._new_button)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setWindowTitle("Terminal")
        self.resize(800, 600)
        self._terms = []
        self.tabCloseRequested[int].connect(self._on_close_request)
        self.currentChanged[int].connect(self._on_current_changed)
        self.connection_address = self.connection_file = None
        
    def setBackendConnections(self, filePath, address):
        self.connection_file = filePath
        self.connection_address = address
        
    def _on_close_request(self, idx):
        term = self.widget(idx)
        term.stop()
        
            
    def _on_current_changed(self, idx):
        term = self.widget(idx)
        self._update_title(term)

    
    def newTerminal(self):
        assert self.connection_file is not None or self.connection_address is not None
        # Create session
        session = Session(parent = self)
        session.connect(connection_file = self.connection_file)
        
        term = TerminalWidget(parent = self)
        term.setSession(session)
        term.session_closed.connect(self._on_session_closed)
        self.addTab(term, "Terminal")
        self._terms.append(term)
        self.setCurrentWidget(term)
        
        session.start(os.environ["SHELL"])
        term.setFocus()

        
    def timerEvent(self, event):
        self._update_title(self.currentWidget())


    def _update_title(self, term):
        if term is None:
            self.setWindowTitle("Terminal")
            return
        idx = self.indexOf(term)
        pid = term.pid()
        self.proc_info.update()
        child_pids = [pid] + self.proc_info.all_children(pid)
        for pid in reversed(child_pids):
            cwd = self.proc_info.cwd(pid)
            if cwd:
                break
        try:
            cmd = self.proc_info.commands[pid]
            title = "%s: %s" % (os.path.basename(cwd), cmd)
        except:
            title = "Terminal"
        title = "Terminal"
        self.setTabText(idx, title)
        self.setWindowTitle(title)

    
    def _on_session_closed(self):
        term = self.sender()
        try:
            self._terms.remove(term)
        except:
            pass
        self.removeTab(self.indexOf(term))
        widget = self.currentWidget()
        if widget:
            widget.setFocus()
        if self.count() == 0:
            self.newTerminal()


class TerminalDock(QtGui.QDockWidget, PMXBaseDock):
    SHORTCUT = "F4"
    ICON = resources.getIcon("utilities-terminal")
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea
    
    #=======================================================================
    # Settings
    #=======================================================================
    SETTINGS_GROUP = 'Terminal'

    @pmxConfigPorperty(default = "linux")
    def colorScheme(self, scheme):
        pass
    
    @pmxConfigPorperty(default = QtGui.QFont("Monospace", 9))
    def font(self, font):
        for index in range(self.tabTerminals.count()):
            self.tabTerminals.widget(index).setFont(font)

    terminalAvailable = True
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.backend = None
        self.setWindowTitle(_("Terminal"))
        self.setObjectName(_("TerminalDock"))
        self.tabTerminals = TabbedTerminal(self)
        self.setWidget(self.tabTerminals)
        self.runBackend()
        
    def runBackend(self):
        self.backend = QtCore.QProcess(self)
        
        self.backend.setWorkingDirectory(os.environ["HOME"])
        
        self.connect(self.backend, QtCore.SIGNAL("readyReadStandardOutput()"),
                     self.write_output)
        self.connect(self.backend, QtCore.SIGNAL("finished(int,QProcess::ExitStatus)"),
                     self.finished)
        
        from prymatex.widgets.pmxterm.backend import main
        self.backend.start(sys.executable, [main.__file__, "-t", "ipc"])    
        self.backend.waitForStarted()
        
        
    def write_output(self):
        data = self.backend.readAllStandardOutput()
        self.tabTerminals.setBackendConnections(*str(data).decode("utf-8").splitlines())
        self.tabTerminals.newTerminal()
        
    def finished(self):
        pass
        
    def initialize(self, mainWindow):
        PMXBaseDock.initialize(self, mainWindow)
        mainWindow.terminal = self
    
    #========================================================
    # Commands
    #========================================================
    def runCommand(self, command):
        if not self.isVisible():
            self.show()
        self.raise_()
        print command
    
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.terminal import PMXTerminalSettings
        return [ PMXTerminalSettings ]
