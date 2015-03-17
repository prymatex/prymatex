#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.core import config

from prymatex.models.trees import FlatTreeProxyModel

class BundleItemProxyTreeModel(QtCore.QSortFilterProxyModel):
    bundleItemTypeOrder = ("bundle", "command", "dragcommand", "syntax",
        "macro", "snippet", "preference", "template", "staticfile", "project")
    def __init__(self, manager, parent = None):
        super(BundleItemProxyTreeModel, self).__init__(parent)
        self.manager = manager
        self.namespaces = (config.PMX_NS_NAME, config.USR_NS_NAME)
        self.bundleItemTypesFilter = self.bundleItemTypeOrder
    
    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = self.sourceModel().node(index)
        if node.isRootNode() or not node.enabled():
            return False
        if self.namespaces:
            if not any([node.hasSource(ns) for ns in self.namespaces]):
                return False
        if self.bundleItemTypesFilter:
            if node.type() not in self.bundleItemTypesFilter:
                return False
        regexp = self.filterRegExp()
        if not (regexp.isEmpty() or node.type() == "bundle"):
            return regexp.indexIn(node.name) != -1
        return True
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
        
    def lessThan(self, left, right):
        leftNode = self.sourceModel().node(left)
        rightNode = self.sourceModel().node(right)
        if leftNode.type() == rightNode.type():
            print(rightNode.name, leftNode.name, rightNode.name > leftNode.name)
            return rightNode.name > leftNode.name
        else:
            return self.bundleItemTypeOrder.index(rightNode.type()) > self.bundleItemTypeOrder.index(leftNode.type())
    
    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:  
            node = self.node(index)
            if node.name != value:
                if node.type() == "bundle":
                    self.manager.updateBundle(node, self.namespaces[-1], name = value)
                elif node.type() == "staticfile":
                    self.manager.updateStaticFile(node, self.namespaces[-1], name = value)
                else:
                    self.manager.updateBundleItem(node, self.namespaces[-1], name = value)
                return True
        return False
        
    def node(self, index):
        return self.sourceModel().node(self.mapToSource(index))
    
    def setFilterNamespace(self, namespaces):
        if isinstance(namespaces, (tuple, list)):
            self.namespaces = namespaces
        else:
            self.namespaces = (config.PMX_NS_NAME, config.USR_NS_NAME)
        self.setFilterRegExp("")
    
    def setFilterBundleItemType(self, bundleItemType):
        if isinstance(bundleItemType, (tuple, list)):
            self.bundleItemTypesFilter = ("bundle") + tuple(bundleItemType)
        else:
            self.bundleItemTypesFilter = self.bundleItemTypeOrder
        self.setFilterRegExp("")

class BundleItemTypeProxyModel(FlatTreeProxyModel):
    def __init__(self, tipos, parent = None):
        super(BundleItemTypeProxyModel, self).__init__(parent)
        self.tipos = tipos if isinstance(tipos, list) else [ tipos ]
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        itemNode = self.sourceModel().node(index)
        return itemNode.type() in self.tipos
        
    def comparableValue(self, index):
        node = self.sourceModel().node(index)
        return node.name.lower()
    
    def compareIndex(self, xindex, yindex):
        xnode = self.sourceModel().node(xindex)
        ynode = self.sourceModel().node(yindex)
        return cmp(xnode.name, ynode.name)
    
class BundleListModel(BundleItemTypeProxyModel):
    def __init__(self, parent = None):
        BundleItemTypeProxyModel.__init__(self, 'bundle', parent)
    
    def data(self, index, role):
        if self.sourceModel() is None:
            return QtCore.QVariant()
        
        if role == QtCore.Qt.CheckStateRole:
            bundle = self.node(index)
            return QtCore.Qt.Checked if bundle.enabled() else QtCore.Qt.Unchecked
        else:
            return BundleItemTypeProxyModel.data(self, index, role)

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
    
class SyntaxListModel(BundleItemTypeProxyModel):
    def __init__(self, parent = None):
        BundleItemTypeProxyModel.__init__(self, 'syntax', parent)
    
    def data(self, index, role):
        if self.sourceModel() is None:
            return None
        
        if not index.isValid():
            return None
        
        sIndex = self.mapToSource(index)
        
        if role == QtCore.Qt.DisplayRole and index.column() == 1:
            syntax = self.sourceModel().node(sIndex)
            return syntax.trigger()
        elif index.column() == 0:
            return self.sourceModel().data(sIndex, role)

    def columnCount(self, parent):
        return 2
    
class TemplateListModel(BundleItemTypeProxyModel):
    def __init__(self, parent = None):
        BundleItemTypeProxyModel.__init__(self, 'template', parent)
    
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

class ProjectListModel(BundleItemTypeProxyModel):
    def __init__(self, parent = None):
        BundleItemTypeProxyModel.__init__(self, 'project', parent)
    
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

class ThemeStyleProxyTableModel(QtCore.QSortFilterProxyModel):
    # ---------------- QtCore.QSortFilterProxyModel overrides
    def filterAcceptsRow(self, sourceRow, sourceParent):
        regexp = self.filterRegExp()
        if regexp.isEmpty():
            return True
        index = self.sourceModel().index(sourceRow, 0, sourceParent)
        node = index.internalPointer()
        return regexp.exactMatch(str(node.styleItem().theme.uuid))

    def lessThan(self, left, right):
        leftData = left.internalPointer()
        rightData = right.internalPointer()
        return rightData.name > leftData.name

    # ------------------ Custom functions
    def style(self, index):
        return self.sourceModel().style(self.mapToSource(index))
        
