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

class GroupTreeNode(TreeNode):
    def __init__(self, name, directory, parent = None):
        self.title = name
        self.directory = directory
        self.identifier = unicode(hash(self.title))
        TreeNode.__init__(self, self.identifier, parent)

    def acceptPath(self, path):
        return os.path.commonprefix([self.directory, path]) == self.directory

    def splitToNamespace(self, path):
        dirName, fileName = os.path.dirname(path), os.path.basename(path)
        return self.identifier + dirName[len(self.directory):], fileName

    @property
    def path(self):
        return os.path.join(self.directory)
    
    @property
    def icon(self):
        return resources.getIcon(self.path)

class FileFoundTreeNode(TreeNode):
    def __init__(self, name, path, parent = None):
        self.title = name
        self.__path = path
        TreeNode.__init__(self, name, parent)
        
    @property
    def path(self):
        return os.path.join(self.__path)
    
    @property
    def icon(self):
        return resources.getIcon(self.path)

class LineTreeNode(TreeNode):
    def __init__(self, line, parent = None):
        self.title = "%s (%s)" % line
        self.identifier = unicode(hash(self.title))
        TreeNode.__init__(self, self.identifier, parent)
        
    @property
    def path(self):
        return os.path.join(self.parentNode.path)
    
    @property
    def icon(self):
        return resources.getIcon(self.path)

#TODO: Poner modelo y proxy en otro lado
class PMXSearchTreeModel(NamespaceTreeModel):
    def __init__(self, parent = None):
        NamespaceTreeModel.__init__(self, separator = os.sep, parent = parent)

    def data(self, index, role):
        node = self.node(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.title
        elif role == QtCore.Qt.DecorationRole:
            return node.icon

    def addGroup(self, name, directory):
        #Estos son los roots, agregar un default group para cuando se busque en otros lugares o el por defecto
        groupNode = GroupTreeNode(name, directory)
        self.addNode(groupNode)
        
    def addFileFound(self, filePath, lines):
        #Buscar coincidencia con grupo para manejar el nombre
        for group in self.rootNode.childrenNodes:
            if group.acceptPath(filePath):
                namespace, fileName = group.splitToNamespace(filePath)
                foundNode = FileFoundTreeNode(fileName, filePath)
                for line in lines:
                    lineNode = LineTreeNode(line)
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