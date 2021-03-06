#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore

class TreeNodeBase(object):
    def __init__(self, nodeName="", nodeParent=None, **kwargs):
        super(TreeNodeBase, self).__init__(**kwargs)
        self.__nodeName = nodeName
        self.__nodeParent = nodeParent
        self.__children = []

    def setNodeName(self, nodeName):
        self.__nodeName = nodeName

    def nodeName(self):
        return self.__nodeName

    def setNodeParent(self, nodeParent):
        self.__nodeParent = nodeParent

    def nodeParent(self):
        return self.__nodeParent
    
    def hasChildren(self):
        return bool(self.__children)
        
    def children(self):
        return self.__children

    def isRootNode(self):
        return self.__nodeParent is None

    def appendChild(self, child):
        self.__children.append(child)
        child.setNodeParent(self)

    def insertChild(self, index, child):
        self.__children.insert(index, child)
        child.setNodeParent(self)

    def removeChild(self, child):
        self.__children.remove(child)
        child.setNodeParent(None)
    
    def findChildByName(self, nodeName):
        for child in self.__children:
            if child.nodeName() == nodeName:
                return child

    def removeAllChildren(self):
        self.__children = []

    def popChild(self, index = -1):
        return self.__children.pop(index)
        
    def childIndex(self, child):
        return self.__children.index(child)
        
    def childrenCount(self):
        return len(self.__children)

    def child(self, row):
        if row < len(self.__children):
            return self.__children[row]
    
    def row(self):
        return self.__nodeParent.childIndex(self)
        
    def column(self):
        return 0

class AbstractTreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, **kwargs):
        super(AbstractTreeModel, self).__init__(**kwargs)
        self.rootNode = self.treeNodeFactory("root", None)

    def treeNodeFactory(self, nodeName, nodeParent):
        return TreeNodeBase(nodeName, nodeParent)

    def rowCount(self, parentIndex):
        return self.node(parentIndex).childrenCount()
        
    def columnCount(self, parentIndex):
        return 1

    def index(self, row, column, parentIndex):
        parentNode = self.node(parentIndex)
        childNode = parentNode.child(row)
        return self.createIndex(row, column, childNode)
    
    def parent(self, index):
        node = self.node(index)
        parentNode = node.nodeParent()
        # Todo ver si puede llegar como index el root porque algo en este if no esta bien
        if parentNode is None or parentNode.isRootNode():
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), parentNode.column(), parentNode)
    
    def indexFromNode(self, node):
        if node.isRootNode():
            return self.createIndex(0, 0, node)
        else:
            return self.createIndex(node.row(), node.column(), node)
    
    def node(self, index):
        if index.isValid():
            return index.internalPointer()
        return self.rootNode
    
    def nodes(self):
        def _collect(node):
            nodes = [ node ]
            if node.childrenCount():
                for child in node.children():
                    nodes.extend(_collect(child))
            return nodes
        return _collect(self.rootNode)

    def findNodes(self, role, value, hits=-1, flags=QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive):
        return [ self.node(index) for index in 
            self.match(self.index(0, 0, QtCore.QModelIndex()), 
                role, value, hits, flags) ]

    def findNode(self, role, value, flags=QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive):
        nodes = self.findNodes(role, value, 1)
        if nodes:
            return nodes[0]

    def clear(self):
        self.rootNode.removeAllChildren()
        self.layoutChanged.emit()
    
    def appendNode(self, node, parent_node=None):
        # TODO: validar y retornar falso si no se puede, ver si el parent puede ser index y node
        parent_node = parent_node or self.rootNode
        parent_index = self.indexFromNode(parent_node)
        self.beginInsertRows(parent_index, parent_node.childrenCount(), parent_node.childrenCount())
        parent_node.appendChild(node)
        self.endInsertRows()
        return True
        
    def removeNode(self, node, parent_node=None):
        # TODO: validar y retornar falso si no se puede, ver si el parent puede ser index y node
        parent_node = parent_node or self.rootNode
        parent_index = self.indexFromNode(parent_node)
        self.beginRemoveRows(parent_index, node.row(), node.row())
        parent_node.removeChild(node)
        self.endRemoveRows()
        return True
        
class AbstractNamespaceTreeModel(AbstractTreeModel):  
    def __init__(self, separator = ".", **kwargs):
        super(AbstractNamespaceTreeModel, self).__init__(**kwargs)
        self.separator = separator
        
    def nodeForNamespace(self, namespace, createProxy=False):
        if not namespace:
            return self.rootNode
        node = self.rootNode
        for name in namespace.split(self.separator):
            if not name:
                raise Exception("No path for %s" % namespace)
            childNode = node.findChildByName(name)
            if childNode is None and createProxy:
                childNode = self.treeNodeFactory(name, node)
                childNode._isproxy = True
                node.appendChild(childNode)
                self.layoutChanged.emit()
            elif childNode is None:
                return None
            node = childNode
        return node
    
    def appendNamespaceNode(self, node):
        return self.insertNamespaceNode("", node)

    def insertNamespaceNode(self, namespace, node):
        parentNode = self.nodeForNamespace(namespace, True)
        parent_inde = self.indexFromNode(parentNode)
        #Check if exit proxy for setting
        proxy = parentNode.findChildByName(node.nodeName())
        if proxy != None:
            if proxy._isproxy:
                #Reparent
                for child in proxy.children():
                    node.appendChild(child)
                parentNode.removeChild(proxy)
            else:
                raise Exception("Node already exists: %s" % node.nodeName())
        parentNode.appendChild(node)
        node._isproxy = False
        self.layoutChanged.emit()
     
#=========================================
# Proxies
#=========================================   
class FlatTreeProxyModel(QtCore.QAbstractItemModel):
    """Proxy for create flat models from tree models"""
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.__indexMap = []
        self.__sourceModel = None

    def sourceModel(self):
        return self.__sourceModel
        
    def setSourceModel(self, model):
        if model == self.__sourceModel:
            return
        if self.__sourceModel is not None:
            self.__sourceModel.disconnect(self)
        self.__sourceModel = model
        self.__sourceModel.dataChanged.connect(self.on_sourceModel_dataChanged)
        self.__sourceModel.rowsInserted.connect(self.on_sourceModel_rowsInserted)
        self.__sourceModel.rowsAboutToBeRemoved.connect(self.on_sourceModel_rowsAboutToBeRemoved)
        self.__sourceModel.layoutChanged.connect(self.on_sourceModel_layoutChanged)
    
    def node(self, index):
        sIndex = self.mapToSource(index)
        node = self.sourceModel().node(sIndex)
        #El root node no puede estar en un flat proxy porque sino no es flat
        if not node.isRootNode():
            return node
    
    def findNode(self, role, value):
        #TODO: Solo si tiene source model y el nodo esta dentro del proxy
        return self.sourceModel().findNode(role, value)
    
    def indexFromNode(self, node):
        source_index = self.sourceModel().indexFromNode(node)
        return self.mapFromSource(source_index)

    def nodes(self):
        return [self.sourceModel().node(index) for index in self.__indexMap]

    def filterAcceptsRow(self, row, parent):
        return True
        
    def filterAcceptsColumn(self, column, parent):
        return True
    
    def mapToSource(self, index):
        if index.isValid():
            return self.__indexMap[index.row()]
        return QtCore.QModelIndex()

    def mapFromSource(self, index):
        if index in self.__indexMap:
            return self.index(self.__indexMap.index(index))
        return QtCore.QModelIndex()
            
    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if self.sourceModel() is not None:
            source_index = self.mapToSource(index)
            return self.sourceModel().data(source_index, role)

    def flags(self, index):
        if self.sourceModel() is None or not index.isValid():  
            return QtCore.Qt.NoItemFlags
        flags = self.sourceModel().flags(self.mapToSource(index))
        #Strip all writable flags and make sure we can select it
        return (flags & ~(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsUserCheckable)) | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        
    def hasChildren(self, index):
        return False

    def index(self, row, column=0, parent=QtCore.QModelIndex()):
        if self.hasIndex(row, column, parent):
            return self.createIndex(row, column)
        return QtCore.QModelIndex()

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, parent):
        return len(self.__indexMap)
    
    # --------------- Source model handler
    def on_sourceModel_dataChanged(self, topLeft, bottomRight):
        if topLeft in self.__indexMap:
            self.dataChanged.emit(self.mapFromSource(topLeft), self.mapFromSource(bottomRight))
    
    def on_sourceModel_rowsInserted(self, parent, start, end):
        for i in range(start, end + 1):
            sIndex = self.sourceModel().index(i, 0, parent)
            if self.filterAcceptsRow(i, parent):
                self.beginInsertRows(QtCore.QModelIndex(), len(self.__indexMap), len(self.__indexMap))
                self.__indexMap.append(sIndex)
                self.endInsertRows()
    
    def on_sourceModel_rowsAboutToBeRemoved(self, parent, start, end):
        #Remove indexes
        for i in range(start, end + 1):
            sIndex = self.sourceModel().index(i, 0, parent)
            if sIndex in self.__indexMap:
                self.beginRemoveRows(QtCore.QModelIndex(), self.__indexMap.index(sIndex), self.__indexMap.index(sIndex))
                self.__indexMap.remove(sIndex)
                self.endRemoveRows()

    def on_sourceModel_layoutChanged(self):
        self.layoutAboutToBeChanged.emit()
        start, end = self.index(0), self.index(len(self.__indexMap))
        print("Update data")
        self.changePersistentIndex(start, end)
        self.layoutChanged.emit()
