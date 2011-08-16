from PyQt4 import QtCore, QtGui
from prymatex.mvc.proxies import PMXFlatBaseProxyModel

class PMXBundleTreeProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        super(PMXBundleTreeProxyModel, self).__init__(parent)
        self.bundleItemTypeOrder = ["bundle", "command", "dragcommand", "macro", "snippet", "preference", "template", "templatefile", "syntax"]
    
    def filterAcceptsRow(self, sourceRow, sourceParent):
        regexp = self.filterRegExp()
        if regexp.isEmpty():
            return True
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        item = index.internalPointer()
        if item.TYPE == "bundle":
            return True
        else:
            #return QtCore.QString(item.TYPE).contains(regexp)
            return True
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
        
    def lessThan(self, left, right):
        leftData = left.internalPointer()
        rightData = right.internalPointer()
        if leftData.TYPE == rightData.TYPE:
            return rightData.name > leftData.name
        else:
            return self.bundleItemTypeOrder.index(rightData.TYPE) > self.bundleItemTypeOrder.index(leftData.TYPE)

class PMXBundleTypeFilterProxyModel(PMXFlatBaseProxyModel):
    def __init__(self, tipos, parent = None):
        super(PMXBundleTypeFilterProxyModel, self).__init__(parent)
        self.tipos = tipos if isinstance(tipos, list) else [ tipos ]
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        item = index.internalPointer()
        return item.TYPE in self.tipos
        
    def compareIndex(self, xindex, yindex):
        xnode = xindex.internalPointer()
        ynode = yindex.internalPointer()
        return cmp(xnode.name, ynode.name)
    
    def findItemIndex(self, item):
        for num, index in enumerate(self.indexMap()):
            if index.internalPointer() == item:
                return num
    
    def getAllItems(self):
        for index in self.indexMap():
            yield index.internalPointer()

class PMXBundleProxyModel(PMXBundleTypeFilterProxyModel):
    def __init__(self, parent = None):
        super(PMXBundleProxyModel, self).__init__('bundle', parent)
    
    def data(self, index, role):
        if self.__sourceModel is None:
            return QtCore.QVariant()
        
        mIndex = self.modelIndex(index)
        row = mIndex.row()
        parent = mIndex.parent()
        
        if role == QtCore.Qt.CheckStateRole:
            index = self.__sourceModel.index(row, 0, parent)
            bundle = index.internalPointer()
            return QtCore.Qt.Checked if bundle.disabled else QtCore.Qt.Unchecked
        else:
            return self.__sourceModel.data(self.__sourceModel.index(row, 0, parent), role)

class PMXSyntaxProxyModel(PMXBundleTypeFilterProxyModel):
    def __init__(self, parent = None):
        super(PMXSyntaxProxyModel, self).__init__('syntax', parent)
    
    def data(self, index, role):
        if self.sourceModel() is None:
            return None
        
        if not index.isValid():
            return None
        
        mIndex = self.modelIndex(index)
        row = mIndex.row()
        parent = mIndex.parent()
        
        if role == QtCore.Qt.DisplayRole and index.column() == 1:
            index = self.sourceModel().index(row, 0, parent)
            syntax = index.internalPointer()
            return syntax.trigger
        elif index.column() == 0:
            return self.sourceModel().data(self.sourceModel().index(row, 0, parent), role)

    def columnCount(self, parent):
        return 2
    
class PMXThemeStyleTableProxyModel(QtGui.QSortFilterProxyModel):
    def filterAcceptsRow(self, sourceRow, sourceParent):
        regexp = self.filterRegExp()
        if regexp.isEmpty():
            return True
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = index.internalPointer()
        return True
        return QtCore.QString(unicode(node.item.theme.uuid)).contains(regexp)
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
        
    def lessThan(self, left, right):
        leftData = left.internalPointer()
        rightData = right.internalPointer()
        return rightData.name > leftData.name
