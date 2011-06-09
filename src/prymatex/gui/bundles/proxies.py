from PyQt4 import QtCore, QtGui
from prymatex.mvc.proxies import PMXFlatBaseProxyModel

class PMXBundleTreeProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        super(PMXBundleTreeProxyModel, self).__init__(parent)
        self.bundleItemTypeOrder = ["bundle", "command", "dragcommand", "macro", "snippet", "preference", "template", "template-file", "syntax"]
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        regexp = self.filterRegExp()
        if regexp.isEmpty():
            return True
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        item = index.internalPointer()
        if item.TYPE == "bundle":
            return True
        else:
            return QtCore.QString(item.TYPE).contains(regexp)
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
        
    def lessThan(self, left, right):
        leftData = left.internalPointer()
        rightData = right.internalPointer()
        if leftData.tipo == rightData.tipo:
            return rightData.name > leftData.name
        else:
            return self.bundleItemTypeOrder.index(rightData.tipo) > self.bundleItemTypeOrder.index(leftData.tipo)

class PMXBundleTypeFilterProxyModel(PMXFlatBaseProxyModel):
    def __init__(self, tipo, parent = None):
        super(PMXBundleTypeFilterProxyModel, self).__init__(parent)
        self.tipo = tipo
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        item = index.internalPointer()
        return item.TYPE == self.tipo
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True

    def compareIndex(self, xindex, yindex):
        xnode = xindex.internalPointer()
        ynode = yindex.internalPointer()
        # Ya son del mismo tipo porque este proxy es por tipo
        return cmp(xnode.name, ynode.name)
    
    def findItem(self, syntax):
        for num, index in enumerate(self.indexMap()):
            if index.internalPointer() == syntax:
                return num