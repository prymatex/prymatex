#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.qt import QtGui, QtCore

from prymatex.core import PrymatexDock

from prymatex import resources
from prymatex.ui.dockers.search import Ui_SearchDock
from prymatex.utils.i18n import ugettext as _
from prymatex.models.search import SearchTreeModel, LineTreeNode
from prymatex.gui.dialogs.filesearch import PMXFileSearchDialog

class SearchResultsDock(PrymatexDock, Ui_SearchDock, QtGui.QDockWidget):
    ICON = "dock-search-results"
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea
    
    def __init__(self, **kwargs):
        super(SearchResultsDock, self).__init__(**kwargs)
        self.setupUi(self)
        self.searchTreeModel = SearchTreeModel(self)
        self.treeView.setModel(self.searchTreeModel)

    def on_actionFileSearch_triggered(self):
        if not self.isVisible():
            self.show()
        self.raise_()
        fileSearch = PMXFileSearchDialog.search(self.searchTreeModel, self)
        #TODO: Si no se encontro nada o se cancelo cerrarlo
    
    @classmethod
    def contributeToMainMenu(cls):
        edit = [
                '-',
                {'text': 'File Search',
                'callback': cls.on_actionFileSearch_triggered }
            ]
        return { "edit": edit }
        
    def on_treeView_activated(self, index):
        node = self.searchTreeModel.node(index)
        if isinstance(node, LineTreeNode):
            self.application.openFile(node.path(), cursorPosition = (node.lineNumber - 1, 0))
    
    def on_treeView_doubleClicked(self, index):
        node = self.searchTreeModel.node(index)
        if isinstance(node, LineTreeNode):
            self.application.openFile(node.path(), cursorPosition = (node.lineNumber - 1, 0))