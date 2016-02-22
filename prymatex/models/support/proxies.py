#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex.core import config

from prymatex.models.trees import FlatTreeProxyModel

class BundleItemProxyTreeModel(QtCore.QSortFilterProxyModel):
    DEFAULT = ("bundle", "command", "dragcommand", "syntax",
        "macro", "snippet", "preference", "template", "staticfile", "project")
    def __init__(self, manager, parent = None):
        super(BundleItemProxyTreeModel, self).__init__(parent)
        self.manager = manager
        self.namespaces = (config.PMX_NS_NAME, config.USR_NS_NAME)
        self.sort_filter_order = self.DEFAULT
    
    def filterAcceptsRow(self, row, parent):
        source_model = self.sourceModel()
        index = source_model.index(row, 0, parent)
        node = source_model.node(index)
        item = node.bundleItem()
        if node.isRootNode() or not item.enabled():
            return False
        if self.namespaces:
            if not any([item.hasSource(ns) for ns in self.namespaces]):
                return False
        if self.sort_filter_order:
            if item.type() not in self.sort_filter_order:
                return False
        regexp = self.filterRegExp()
        if not (regexp.isEmpty() or item.type() == "bundle"):
            return regexp.indexIn(item.name) != -1
        return True
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
        
    def lessThan(self, left, right):
        source_model = self.sourceModel()
        left_node = source_model.node(left)
        right_node = source_model.node(right)
        left_item = left_node.bundleItem()
        right_item = right_node.bundleItem()
        if left_item.type() == right_item.type():
            return right_node.nodeName() > left_node.nodeName()
        else:
            return self.sort_filter_order.index(right_item.type()) > self.sort_filter_order.index(left_item.type())
    
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
    
    def setFilterBundleItemTypes(self, types):
        if types and isinstance(types, (tuple, list)):
            self.sort_filter_order = ("bundle", ) + tuple(types)
        else:
            self.sort_filter_order = self.DEFAULT
        self.setFilterRegExp("")

class BundleItemTypeListModel(FlatTreeProxyModel):
    def __init__(self, types, parent=None):
        super(BundleItemTypeListModel, self).__init__(parent)
        self.types = types

    def filterAcceptsRow(self, row, parent):
        source_model = self.sourceModel()
        index = source_model.index(row, 0, parent)
        node = source_model.node(index)
        item = node.bundleItem()
        return item.type() in self.types

class BundleListModel(BundleItemTypeListModel):
    def __init__(self, parent=None):
        BundleItemTypeListModel.__init__(self, ('bundle', ), parent)
    
    def data(self, index, role):
        if not index.isValid() or self.sourceModel() is None:
            return None
        
        if role == QtCore.Qt.CheckStateRole:
            node = self.node(index)
            item = node.bundleItem()
            return QtCore.Qt.Checked if item.enabled() else QtCore.Qt.Unchecked
        else:
            return BundleItemTypeListModel.data(self, index, role)

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
    
class SyntaxListModel(BundleItemTypeListModel):
    def __init__(self, parent = None):
        BundleItemTypeListModel.__init__(self, ('syntax', ), parent)

    def data(self, index, role):
        if not index.isValid() or self.sourceModel() is None:
            return None
        
        sIndex = self.mapToSource(index)
        
        if role == QtCore.Qt.DisplayRole and index.column() == 1:
            syntax = self.sourceModel().node(sIndex)
            return syntax.trigger()
        elif index.column() == 0:
            return self.sourceModel().data(sIndex, role)

    def columnCount(self, parent):
        return 2
    
class TemplateListModel(BundleItemTypeListModel):
    def __init__(self, parent = None):
        BundleItemTypeListModel.__init__(self, ('template', ), parent)
    
    def data(self, index, role):
        if not index.isValid() or self.sourceModel() is None:
            return None
        
        sIndex = self.mapToSource(index)
        
        if role == QtCore.Qt.DisplayRole and index.column() == 1:
            node = self.sourceModel().node(sIndex)
            item = node.bundleItem()
            return item.bundle.name
        elif index.column() == 0:
            return self.sourceModel().data(sIndex, role)

    def columnCount(self, parent):
        return 2

class ProjectListModel(BundleItemTypeListModel):
    def __init__(self, parent = None):
        BundleItemTypeListModel.__init__(self, ('project', ), parent)
    
    def data(self, index, role):
        if not index.isValid() or self.sourceModel() is None:
            return None
        
        sIndex = self.mapToSource(index)
        
        if role == QtCore.Qt.DisplayRole and index.column() == 1:
            node = self.sourceModel().node(sIndex)
            item = node.bundleItem()
            return item.bundle.name
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
        source_model = self.sourceModel()
        index = source_model.index(sourceRow, 0, sourceParent)
        item = source_model.style(index)
        return regexp.exactMatch(item.styleItem().theme.uuidAsText())

    def lessThan(self, left, right):
        source_model = self.sourceModel()
        left_item = source_model.style(left)
        right_item = source_model.style(right)
        return right_item.styleItem().name > left_item.styleItem().name

    # ------------------ Custom functions
    def style(self, index):
        return self.sourceModel().style(self.mapToSource(index))

