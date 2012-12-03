#-*- encoding: utf-8 -*-

import os, sys

from prymatex.qt import QtCore, QtGui

from prymatex.core import PMXBaseDock

from prymatex import resources
from prymatex.core.settings import pmxConfigPorperty
from prymatex.utils.i18n import ugettext as _
from prymatex.utils.misc import get_home_dir
from prymatex.widgets.pmxterm import BackendManager, TerminalWidget


class TabbedTerminal(QtGui.QTabWidget):

    
    def __init__(self, parent=None):
        super(TabbedTerminal, self).__init__(parent)
        #Solo si no es windows
        #self.proc_info = ProcessInfo()
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
        # Create session
        session = self.parent().localBackend.session()
        term = TerminalWidget(session, parent = self)
        term.sessionClosed.connect(self._on_session_closed)
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
        #Solo si no es windows
        #self.proc_info.update()
        #child_pids = [pid] + self.proc_info.all_children(pid)
        #for pid in reversed(child_pids):
        #    cwd = self.proc_info.cwd(pid)
        #    if cwd:
        #        break
        #try:
        #    cmd = self.proc_info.commands[pid]
        #    title = "%s: %s" % (os.path.basename(cwd), cmd)
        #except:
        #    title = "Terminal"
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
        self.backendManager = BackendManager(parent = self)
        self.localBackend = self.backendManager.localBackend(workingDirectory = get_home_dir())
        
        
    def finished(self):
        pass
        
    def initialize(self, mainWindow):
        PMXBaseDock.initialize(self, mainWindow)
        mainWindow.terminal = self
        self.tabTerminals.newTerminal()
        
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
