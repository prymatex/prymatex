#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from PyQt4 import QtGui, QtCore

from prymatex import resources
from prymatex.ui.dockers.search import Ui_SearchDock
from prymatex.core.plugin.dock import PMXBaseDock
from prymatex.utils.i18n import ugettext as _
from prymatex.models.tree import NamespaceTreeModel, TreeNode

from prymatex.gui.dialogs.filesearch import PMXFileSearchDialog

#TODO: Poner modelo y proxy en otro lado
class PMXSearchTreeModel(NamespaceTreeModel):
    def __init__(self, parent = None):
        NamespaceTreeModel.__init__(self, separator = os.sep, parent = parent)

    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.name
        elif role == QtCore.Qt.DecorationRole:
            return None

    def addGroup(self, name, directory):
        #Estos son los roots
        groupNode = TreeNode(name)
        groupNode.directory = directory
        self.addNode(groupNode)
        
    def addFileFound(self, filePath, lines):
        #Buscar coincidencia con grupo para manejar el nombre
        for group in self.rootNode.childrenNodes:
            if os.path.commonprefix([group.directory, filePath]) == group.directory:
                dirName, fileName = os.path.dirname(filePath), os.path.basename(filePath)
                namespace = group.name + dirName[len(group.directory):]
                foundNode = TreeNode(fileName)
                for line in lines:
                    lineNode = TreeNode(line)
                    foundNode.appendChild(lineNode)
                self.addNamespaceNode(namespace, foundNode)
                

class PMXSearchDock(QtGui.QDockWidget, Ui_SearchDock, PMXBaseDock):
    SHORTCUT = "Shift+F4"
    ICON = resources.getIcon("find")
    PREFERED_AREA = QtCore.Qt.BottomDockWidgetArea
    
    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
        PMXBaseDock.__init__(self)
        self.setupUi(self)
        self.searchTreeModel = PMXSearchTreeModel(self)
        self.treeView.setModel(self.searchTreeModel)

    def on_actionFileSearch_triggered(self):
        if not self.isVisible():
            self.show()
        self.raise_()
        fileSearch = PMXFileSearchDialog.search(self.searchTreeModel, self)
        #TODO: Si no se encontro nada o se cancelo cerrarlo
    
    @classmethod
    def contributeToMainMenu(cls):
        edit = {
            'items': [
                "-",
                {'title': "File Search",
                 'callback': cls.on_actionFileSearch_triggered }
            ]}
        return { "Edit": edit }