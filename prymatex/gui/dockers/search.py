#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.core.plugin.dock import PMXBaseDock
from prymatex.utils.i18n import ugettext as _

from prymatex.gui.dialogs.filefind import PMXFileFindDialog

class PMXSearchDock(QtGui.QDockWidget, PMXBaseDock):
    SHORTCUT = "Shift+F4"
    ICON = resources.getIcon("console")
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea
    
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setWindowTitle(_("Search"))
        self.setObjectName(_("SearchDock"))
        self.setupConsole()

    def setupConsole(self):
        self.console = QtGui.QPushButton("File Find", self)
        self.console.pressed.connect(self.on_button_pressed)
        self.setWidget(self.console)
        
    def on_button_pressed(self):
        fileFind = PMXFileFindDialog(self)
        fileFind.exec_()
