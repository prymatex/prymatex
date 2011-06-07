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
        if item.tipo == "bundle":
            return True
        else:
            return QtCore.QString(item.tipo).contains(regexp)
        
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
        return item.tipo == self.tipo
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True

