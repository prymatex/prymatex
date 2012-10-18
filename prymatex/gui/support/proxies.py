#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from prymatex.models.proxies import FlatTreeProxyModel

class PMXBundleTreeProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, manager, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.manager = manager
        self.bundleItemTypeOrder = ["bundle", "command", "dragcommand", "macro", "snippet", "preference", "template", "templatefile", "syntax", "project"]
        self.namespacesFilter = [ "prymatex", "user" ]
        self.bundleItemTypesFilter = self.bundleItemTypeOrder[:]
    
    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = self.sourceModel().node(index)
        if node.isRootNode() or not node.enabled:
            return False
        if self.namespacesFilter:
            if not any(map(lambda ns: node.hasNamespace(ns), self.namespacesFilter)):
                return False
        if self.bundleItemTypesFilter:
            if node.TYPE not in self.bundleItemTypesFilter:
                return False
        regexp = self.filterRegExp()
        if not (regexp.isEmpty() or node.TYPE == "bundle"):
            return regexp.indexIn(node.name) != -1
        return True
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
        
    def lessThan(self, left, right):
        leftNode = self.sourceModel().node(left)
        rightNode = self.sourceModel().node(right)
        if leftNode.TYPE == rightNode.TYPE:
            return rightNode.name > leftNode.name
        else:
            return self.bundleItemTypeOrder.index(rightNode.TYPE) > self.bundleItemTypeOrder.index(leftNode.TYPE)
    
    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:  
            node = self.node(index)
            if node.TYPE == "bundle":
                self.manager.updateBundle(node, self.namespacesFilter[-1], name = value)
            elif node.TYPE == "templatefile":
                self.manager.updateTemplateFile(node, self.namespacesFilter[-1], name = value)
            else:
                self.manager.updateBundleItem(node, self.namespacesFilter[-1], name = value)
            return True
        return False
        
    def node(self, index):
        sIndex = self.mapToSource(index)
        return self.sourceModel().node(sIndex)
    
    def setFilterNamespace(self, namespace):
        if namespace:
            self.namespacesFilter = [ namespace ]
        else:
            self.namespacesFilter = [ "prymatex", "user" ]
        self.setFilterRegExp("")
    
    def setFilterBundleItemType(self, bundleItemType):
        if bundleItemType:
            self.bundleItemTypesFilter = [ "bundle" ] + bundleItemType.split()
        else:
            self.bundleItemTypesFilter = self.bundleItemTypeOrder[:]
        self.setFilterRegExp("")

class PMXBundleTypeFilterProxyModel(FlatTreeProxyModel):
    def __init__(self, tipos, parent = None):
        FlatTreeProxyModel.__init__(self, parent)
        self.tipos = tipos if isinstance(tipos, list) else [ tipos ]
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        item = index.internalPointer()
        return item.TYPE in self.tipos
        
    def comparableValue(self, index):
        node = self.sourceModel().node(index)
        #Esto es para rastrear un error
        try:
            return node.name.lower()
        except Exception, e:
            print node, self.sourceModel(), index
    
    def compareIndex(self, xindex, yindex):
        xnode = xindex.internalPointer()
        ynode = yindex.internalPointer()
        return cmp(xnode.name, ynode.name)
    
    def findItemIndex(self, item):
        for num, index in enumerate(self.indexMap()):
            if index.internalPointer() == item:
                return num
    
    def getAllItems(self):
        items = []
        for index in self.indexMap():
            items.append(index.internalPointer())
        return items

class PMXBundleProxyModel(PMXBundleTypeFilterProxyModel):
    def __init__(self, parent = None):
        super(PMXBundleProxyModel, self).__init__('bundle', parent)
    
    def data(self, index, role):
        if self.sourceModel() is None:
            return QtCore.QVariant()
        
        sIndex = self.mapToSource(index)
        if role == QtCore.Qt.CheckStateRole:
            bundle = sIndex.internalPointer()
            return QtCore.Qt.Checked if bundle.enabled else QtCore.Qt.Unchecked
        else:
            return self.sourceModel().data(sIndex, role)

    def setData(self, index, value, role):
        if self.sourceModel() is None:
            return False
            
        sIndex = self.mapToSource(index)    
        if role == QtCore.Qt.CheckStateRole:
            return self.sourceModel().setData(sIndex, value, role)
        return False

    def columnCount(self, parent):
        return 1
    
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
    
class PMXSyntaxProxyModel(PMXBundleTypeFilterProxyModel):
    def __init__(self, parent = None):
        PMXBundleTypeFilterProxyModel.__init__(self, 'syntax', parent)
    
    def data(self, index, role):
        if self.sourceModel() is None:
            return None
        
        if not index.isValid():
            return None
        
        sIndex = self.mapToSource(index)
        
        if role == QtCore.Qt.DisplayRole and index.column() == 1:
            syntax = self.sourceModel().node(sIndex)
            return syntax.trigger
        elif index.column() == 0:
            return self.sourceModel().data(sIndex, role)

    def columnCount(self, parent):
        return 2
    
class PMXTemplateProxyModel(PMXBundleTypeFilterProxyModel):
    def __init__(self, parent = None):
        PMXBundleTypeFilterProxyModel.__init__(self, 'template', parent)
    
    def data(self, index, role):
        if self.sourceModel() is None:
            return None
        
        if not index.isValid():
            return None
        
        sIndex = self.mapToSource(index)
        
        if role == QtCore.Qt.DisplayRole and index.column() == 1:
            template = self.sourceModel().node(sIndex)
            return template.bundle.name
        elif index.column() == 0:
            return self.sourceModel().data(sIndex, role)

    def columnCount(self, parent):
        return 2

class PMXProjectProxyModel(PMXBundleTypeFilterProxyModel):
    def __init__(self, parent = None):
        PMXBundleTypeFilterProxyModel.__init__(self, 'project', parent)
    
    def data(self, index, role):
        if self.sourceModel() is None:
            return None
        
        if not index.isValid():
            return None
        
        sIndex = self.mapToSource(index)
        
        if role == QtCore.Qt.DisplayRole and index.column() == 1:
            template = self.sourceModel().node(sIndex)
            return template.bundle.name
        elif index.column() == 0:
            return self.sourceModel().data(sIndex, role)

    def columnCount(self, parent):
        return 2

class PMXThemeStyleTableProxyModel(QtGui.QSortFilterProxyModel):
    def filterAcceptsRow(self, sourceRow, sourceParent):
        regexp = self.filterRegExp()
        if regexp.isEmpty():
            return True
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = index.internalPointer()
        return regexp.exactMatch(unicode(node.item.theme.uuid))
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
        
    def lessThan(self, left, right):
        leftData = left.internalPointer()
        rightData = right.internalPointer()
        return rightData.name > leftData.name
