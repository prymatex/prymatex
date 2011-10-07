import os
from PyQt4 import QtCore, QtGui

def orderFileByName(left, right, folderFirst):
    isldir = os.path.isdir(left)
    isrdir = os.path.isdir(right)
    if folderFirst and isldir and not isrdir:
        return True
    elif folderFirst and not isldir and isrdir:
        return False
    else:
        return left < right

def orderFileBySize(left, right, folderFirst):
    isldir = os.path.isdir(left)
    isrdir = os.path.isdir(right)
    if folderFirst and isldir and not isrdir:
        return True
    elif folderFirst and not isldir and isrdir:
        return False
    elif isldir and isrdir:
        return left < right
    else:
        return os.path.getsize(left) > os.path.getsize(right)

def orderFileByDate(left, right, folderFirst):
    isldir = os.path.isdir(left)
    isrdir = os.path.isdir(right)
    if folderFirst and isldir and not isrdir:
        return True
    elif folderFirst and not isldir and isrdir:
        return False
    elif isldir and isrdir:
        return left < right
    else:
        return os.path.getctime(left) > os.path.getctime(right)

def orderFileByType(left, right, folderFirst):
    isldir = os.path.isdir(left)
    isrdir = os.path.isdir(right)
    if folderFirst and isldir and not isrdir:
        return True
    elif folderFirst and not isldir and isrdir:
        return False
    elif isldir and isrdir:
        return left < right
    else:
        return os.path.splitext(left)[-1] > os.path.splitext(right)[-1]

ORDERS = {"name": orderFileByName, "type": orderFileByType, "date": orderFileByDate, "size": orderFileBySize}

class PMXFileSystemProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        super(PMXFileSystemProxyModel, self).__init__(parent)
        self.orderBy = "name"
        self.folderFirst = True
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        sIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
        path = self.sourceModel().filePath(sIndex)
        return True
    
    def columnCount(self, parent):
        return 1
        
    def lessThan(self, left, right):
        leftPath = self.sourceModel().filePath(left)
        rightPath = self.sourceModel().filePath(right)
        return ORDERS[self.orderBy](leftPath, rightPath, self.folderFirst)

    def sortBy(self, orderBy, folderFirst = True, descending = False):
        order = QtCore.Qt.AscendingOrder if not descending else QtCore.Qt.DescendingOrder
        self.orderBy = orderBy
        self.folderFirst = folderFirst
        QtGui.QSortFilterProxyModel.sort(self, 0, order)
        