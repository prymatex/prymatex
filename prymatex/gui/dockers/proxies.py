import os
import fnmatch
from PyQt4 import QtCore, QtGui

def orderFileByName(left, right):
    return left < right

def orderFileBySize(left, right):
    return os.path.getsize(left) > os.path.getsize(right)

def orderFileByDate(left, right):
    return os.path.getctime(left) > os.path.getctime(right)

def orderFileByType(left, right):
    return os.path.splitext(left)[-1] > os.path.splitext(right)[-1]

ORDERS = {"name": orderFileByName, "type": orderFileByType, "date": orderFileByDate, "size": orderFileBySize}

class PMXFileSystemProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        super(PMXFileSystemProxyModel, self).__init__(parent)
        self.orderBy = "name"
        self.folderFirst = True
        self.descending = False
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        sIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
        path = self.sourceModel().filePath(sIndex)
        regexp = self.filterRegExp()
        if not regexp.isEmpty():
            pattern = regexp.pattern()
            accept = any(map(lambda p: fnmatch.fnmatch(path, p), map(lambda p: p.strip(), pattern.split(",")))) if not os.path.isdir(path) else True
            return accept
        return True
    
    def columnCount(self, parent):
        return 1
        
    def lessThan(self, left, right):
        isleftdir = self.sourceModel().isDir(left)
        isrightdir = self.sourceModel().isDir(right)
        if self.folderFirst and isleftdir and not isrightdir:
            return not self.descending
        elif self.folderFirst and not isleftdir and isrightdir:
            return self.descending
        else:
            leftPath = self.sourceModel().filePath(left)
            rightPath = self.sourceModel().filePath(right)
            return ORDERS[self.orderBy](leftPath, rightPath)

    def sortBy(self, orderBy, folderFirst = True, descending = False):
        order = QtCore.Qt.AscendingOrder if not descending else QtCore.Qt.DescendingOrder
        self.orderBy = orderBy
        self.folderFirst = folderFirst
        self.descending = descending
        QtGui.QSortFilterProxyModel.sort(self, 0, order)
        
    def filePath(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().filePath(sIndex)