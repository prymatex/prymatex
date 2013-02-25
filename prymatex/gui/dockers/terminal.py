#-*- encoding: utf-8 -*-

import os, sys
import random

from prymatex.qt import QtCore, QtGui

from prymatex import resources

from prymatex.core import config
from prymatex.core import PMXBaseDock
from prymatex.core.settings import pmxConfigPorperty
from prymatex.utils.i18n import ugettext as _
from prymatex.utils.misc import get_home_dir

from prymatex.widgets.pmxterm import Backend, BackendManager, TerminalWidget, ColorScheme


SHEME_SCOPES = [ 'comment', 'string', 'constant.numeric', 'constant.language', 
    'constant.character, constant.other', 'variable.language, variable.other',
    'keyword', 'storage', 'entity.name.class', 'entity.other.inherited-class',
    'entity.name.function', 'variable.parameter', 'entity.name.tag',
    'entity.other.attribute-name', 'support.function', 'support.constant',
    'support.type, support.class', 'support.other.variable', 'invalid' ]

# Load color schemes
ColorScheme.loadSchemes(os.path.join(config.PMX_SHARE_PATH, "Schemes"))

class TabbedTerminal(QtGui.QTabWidget):
    
    def __init__(self, parent=None):
        super(TabbedTerminal, self).__init__(parent)
        self.setTabPosition(QtGui.QTabWidget.South)
        self._new_button = QtGui.QPushButton(self)
        self._new_button.setText("New")
        self._new_button.clicked.connect(lambda checked: self.newTerminal())
        self.setCornerWidget(self._new_button)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested[int].connect(self._on_close_request)
        self.currentChanged[int].connect(self._on_current_changed)
        
    def _on_close_request(self, idx):
        term = self.widget(idx)
        term.stop()
        
            
    def _on_current_changed(self, idx):
        term = self.widget(idx)
        self._update_title(term)

    
    def currentTerminal(self):
        return self.currentWidget()
    
    def newTerminal(self, session = None):
        # Create session
        if session is None and self.parent().backend.state() == Backend.Running:
            session = self.parent().backend.session()
        if session is not None:
            term = TerminalWidget(session, scheme = self.parent().colorScheme(), parent = self)
            term.sessionClosed.connect(self._on_session_closed)
            self.addTab(term, "Terminal")
            self.setCurrentWidget(term)
            session.start()
            term.setFocus()
        
        
    def timerEvent(self, event):
        self._update_title(self.currentWidget())


    def _update_title(self, term):
        if term is None:
            self.setWindowTitle("Terminal")
            return
        idx = self.indexOf(term)
        title = "Terminal"
        self.setTabText(idx, title)
        self.setWindowTitle(title)

    
    def _on_session_closed(self):
        term = self.sender()
        self.removeTab(self.indexOf(term))
        widget = self.currentWidget()
        if widget:
            widget.setFocus()
        if self.count() == 0:
            self.newTerminal()

    def setColorScheme(self, scheme):
        for index in range(self.count()):
            self.widget(index).setColorScheme(scheme)


class TerminalDock(QtGui.QDockWidget, PMXBaseDock):
    SHORTCUT = "F4"
    ICON = resources.getIcon("utilities-terminal")
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea

    
    # ------------------ Settings
    SETTINGS_GROUP = 'Terminal'

    @pmxConfigPorperty(default = "default")
    def defaultScheme(self, name):
        scheme = ColorScheme.scheme(name)
        for index in range(self.tabTerminals.count()):
            self.tabTerminals.widget(index).setColorScheme(scheme)
    
    @pmxConfigPorperty(default = QtGui.QFont("Monospace", 9))
    def defaultFont(self, font):
        for index in range(self.tabTerminals.count()):
            self.tabTerminals.widget(index).setFont(font)

    @pmxConfigPorperty(default = False)
    def editorTheme(self, value):
        if value:
            self.application.registerSettingHook("CodeEditor.defaultTheme", self.on_defaultTheme_changed)
        else:
            self.application.unregisterSettingHook("CodeEditor.defaultTheme", self.on_defaultTheme_changed)
            

    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setWindowTitle(_("Terminal"))
        self.setObjectName(_("TerminalDock"))
        self.tabTerminals = TabbedTerminal(self)
        self.setWidget(self.tabTerminals)
        
        # Manager
        self.backendManager = BackendManager(parent = self)
        self.application.aboutToQuit.connect(self.backendManager.closeAll)
        
        # Local Backend
        self.backend = self.backendManager.localBackend()
        self.backend.started.connect(self.tabTerminals.newTerminal)
        self.backend.start()
        
        # Color scheme
        self.__editorColorScheme = None
        

    def initialize(self, mainWindow):
        PMXBaseDock.initialize(self, mainWindow)
        mainWindow.terminal = self

    # ---------------- Scheme
    def colorScheme(self):
        return self.__editorColorScheme if self.editorTheme else ColorScheme.scheme(self.defaultScheme)

    # ---------------- Settings hooks
    def on_defaultTheme_changed(self, themeUUID):
        theme = self.application.supportManager.getTheme(themeUUID)
        self.__editorColorScheme = ColorScheme(theme.name)
        
        # Foreground and background
        self.__editorColorScheme.setBackground(theme.settings["background"])
        self.__editorColorScheme.setBackground(theme.settings["selection"], intense = True)
        self.__editorColorScheme.setForeground(theme.settings["foreground"])
        self.__editorColorScheme.setForeground(theme.settings["lineHighlight"], intense = True)
        
        # Mapping scopes :)
        scopes = SHEME_SCOPES[:]
        random.shuffle(scopes)
        scopes = scopes[:16]
        for index, scope in enumerate(scopes[:8]):
            self.__editorColorScheme.setColor(index, theme.getStyle(scope)["foreground"])
        for index, scope in enumerate(scopes[8:]):
            self.__editorColorScheme.setColor(index, theme.getStyle(scope)["foreground"], intense = True)
        
        self.tabTerminals.setColorScheme(self.__editorColorScheme)
        
    # ---------------- Commands
    def runCommand(self, command):
        self.sendCommand(command)
    
    def sendCommand(self, command):
        if not self.isVisible():
            self.show()
        self.raise_()
        self.tabTerminals.currentTerminal().send("%s\n" % command)
        
    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.terminal import PMXTerminalSettings
        return [ PMXTerminalSettings ]
