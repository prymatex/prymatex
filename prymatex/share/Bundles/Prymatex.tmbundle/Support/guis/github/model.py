#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

GITHUB_CLONE_URL = 'https://github.com/{username}/{name}.git'

class RepositoryTableModel(QtCore.QAbstractTableModel):
    HEADER_NAMES = ["Name", "User", "Watchers"]
    def __init__(self, parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.repositories = []
        
    def rowCount(self, parent = None):
        return len(self.repositories)
    
    def columnCount(self, parent = None):
        return len(self.HEADER_NAMES)
        
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.HEADER_NAMES[section]
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid(): 
            return None
        repository = self.repositories[ index.row() ]
        
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            return QtCore.Qt.Checked if repository['checked'] else QtCore.Qt.Unchecked
        elif role in [ QtCore.Qt.DisplayRole, QtCore.Qt.EditRole ]:
            if index.column() == 0:
                return repository['name']
            elif index.column() == 1:
                return repository['username']
            elif index.column() == 2:
                return repository['watchers']

    def setData(self, index, value, role):
        """Retornar verdadero si se puedo hacer el cambio, falso en caso contrario"""

        if not index.isValid(): return False
        repository = self.repositories[ index.row() ]
        
        if role == QtCore.Qt.CheckStateRole:
            repository['checked'] = value
            self.dataChanged.emit(index, index)
            return True
        return False
    
    def hasSelected(self):
        return bool(self.allSelected())
        
    def allSelected(self):
        return [repo for repo in self.repositories if repo["checked"]]
        
    def clearUnselected(self):
        self.repositories = [repo for repo in self.repositories if repo["checked"]]
        self.layoutChanged.emit()
        
    def addRepositories(self, repositories):
        for repo in repositories:
            repo['checked'] = False
            if repo["name"].endswith(".tmbundle") or repo["name"].endswith("-tmbundle"):
                basename = "%s.tmbundle" % repo["name"][0:-9]
            else:
                basename = "%s.tmbundle" % repo["name"]
            repo['folder'] = basename
            repo.setdefault('homepage', '')
            repo.setdefault('url', GITHUB_CLONE_URL.format(**repo))
            repo.setdefault('namespace', None)
        self.repositories += repositories
        self.layoutChanged.emit()
    
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
        
class RepositoryProxyTableModel(QtGui.QSortFilterProxyModel):
    def filterAcceptsRow(self, sourceRow, sourceParent):
        return True
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
        
    def lessThan(self, left, right):
        source = self.sourceModel()
        leftRepo = source.repositories[left.row()]
        rightRepo = source.repositories[right.row()]
        if self.sortColumn() == 0:
            return leftRepo["name"] > rightRepo["name"]
        elif self.sortColumn() == 1:
            return leftRepo["username"] > rightRepo["username"]
        elif self.sortColumn() == 2:
            return leftRepo["watchers"] > rightRepo["watchers"]