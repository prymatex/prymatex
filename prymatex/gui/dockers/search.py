#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.ui.dockers.search import Ui_SearchDock
from prymatex.core.plugin.dock import PMXBaseDock
from prymatex.utils.i18n import ugettext as _

from prymatex.gui.dialogs.filesearch import PMXFileSearchDialog

class PMXSearchDock(QtGui.QDockWidget, Ui_SearchDock, PMXBaseDock):
    SHORTCUT = "Shift+F4"
    ICON = resources.getIcon("find")
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea
    
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setupUi(self)

    def on_actionFileSearch_triggered(self):
        fileSearch = PMXFileSearchDialog(self)
        fileSearch.exec_()
    
    @classmethod
    def contributeToMainMenu(cls):
        edit = {
            'items': [
                "-",
                {'title': "File Search",
                 'callback': cls.on_actionFileSearch_triggered }
            ]}
        return { "Edit": edit }