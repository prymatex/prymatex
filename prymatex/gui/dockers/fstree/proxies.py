import os
from PyQt4 import QtCore, QtGui

class PMXFileSystemProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        super(PMXFileSystemProxyModel, self).__init__(parent)
        self.setDynamicSortFilter(True)
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        sIndex = self.sourceModel().index(sourceRow, 0, sourceParent)
        path = self.sourceModel().filePath(sIndex)
        return True
    
    def columnCount(self, parent):
        return 1
        
    def lessThan(self, left, right):
        leftPath = self.sourceModel().filePath(left)
        rightPath = self.sourceModel().filePath(right)
        if os.path.isdir(leftPath) and not os.path.isdir(rightPath):
            return False
        elif not os.path.isdir(leftPath) and os.path.isdir(rightPath):
            return True
        else:
            return left > right
