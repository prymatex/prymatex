#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore

from prymatex.utils.lists import bisect_key

class TreeNode(object):
    def __init__(self, nodeName, nodeParent = None):
        #TODO: Migrar a atributos ocultos __childrenNodes
        self.setNodeName(nodeName)
        self.setNodeParent(nodeParent)
        self.childrenNodes = []
    
    def setNodeName(self, name):
        self.__nodeName = name
        
    def nodeName(self):
        return self.__nodeName
        
    def setNodeParent(self, parent):
        self.__nodeParent = parent
        
    def nodeParent(self):
        return self.__nodeParent
        
    def isRootNode(self):
        return self.nodeParent() == None
    
    def appendChild(self, child):
        self.childrenNodes.append(child)
        child.setNodeParent(self)

    def insertChild(self, index, child):
        self.childrenNodes.insert(index, child)
        child.setNodeParent(self)

    def removeChild(self, child):
        self.childrenNodes.remove(child)
        child.setNodeParent(None)
    
    def findChildByName(self, nodeName):
        for child in self.childrenNodes:
            if child.nodeName() == nodeName:
                return child

    def removeAllChild(self):
        for child in self.childrenNodes:
            self.removeChild(child)

    def childIndex(self, child):
        return self.childrenNodes.index(child)
        
    def childCount(self):
        return len(self.childrenNodes)

    def child(self, row):
        if row < len(self.childrenNodes):
            return self.childrenNodes[row]
    
    def row(self):
        return self.nodeParent().childIndex(self)

class TreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.rootNode = self.treeNodeFactory("root")

    def treeNodeFactory(self, nodeName, nodeParent = None):
        return TreeNode(nodeName, nodeParent)

    def rowCount(self, parent):
        parentNode = self.node(parent)
        return parentNode.childCount()
    
    def columnCount(self, parent):
        return 1  

    def index(self, row, column, parent):
        parentNode = self.node(parent)
        childNode = parentNode.child(row)
        if childNode is not None:
            return self.createIndex(row, column, childNode)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        node = self.node(index)
        parentNode = node.nodeParent()
        if parentNode is None or parentNode.isRootNode():
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)
    
    def node(self, index = QtCore.QModelIndex()):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.rootNode
    
    def clear(self):
        self.rootNode.removeAllChild()
        self.layoutChanged.emit()
        
class NamespaceTreeModel(TreeModel):  
    def __init__(self, separator = ".", parent = None):
        TreeModel.__init__(self, parent)
        self.separator = separator
        
    def nodeForNamespace(self, namespace, createProxy = False):
        node = self.rootNode
        names = namespace.split(self.separator)
        for name in names:
            if name != "":
                nextNode = node.findChildByName(name)
                if nextNode is None and createProxy:
                    nextNode = self.treeNodeFactory(name, node)
                    nextNode._isproxy = True
                    node.appendChild(nextNode)
                    self.layoutChanged.emit()
                elif nextNode is None:
                    return None
                node = nextNode
        return node
    
    def addNode(self, node):
        return self.addNamespaceNode("", node)

    def addNamespaceNode(self, namespace, node):
        parentNode = self.nodeForNamespace(namespace, True)
        parentIndex = self.createIndex(parentNode.row(), 0, parentNode) if not parentNode.isRootNode() else QtCore.QModelIndex()
        #Check if exit proxy for setting
        proxy = parentNode.findChildByName(node.nodeName())
        if proxy != None:
            if proxy._isproxy:
                #Reparent
                for child in proxy.childrenNodes:
                    node.appendChild(child)
                parentNode.removeChild(proxy)
                self.layoutChanged.emit()
            else:
                raise Exception("Node Already Exists" % node.nodeName())
        self.beginInsertRows(parentIndex, node.childCount(), node.childCount())
        parentNode.appendChild(node)
        node._isproxy = False
        self.endInsertRows()
     
#=========================================
# Proxies
#=========================================   
class FlatTreeProxyModel(QtCore.QAbstractItemModel):
    """
    Proxy for create flat models from tree models
    """
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.__indexMap = []
        self.__sourceModel = None

    def indexMap(self):
        return self.__indexMap
    
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
        
    def filterAcceptsRow(self, sourceRow, sourceParent):
        return True
        
    def filterAcceptsColumn(self, sourceColumn, sourceParent):
        return True
    
    def comparableValue(self, index):
        return 0
        
    def compareIndex(self, xindex, yindex):
        return 0
    
    def mapToSource(self, proxyIndex):
        return self.__indexMap[proxyIndex.row()]

    def mapFromSource(self, sourceIndex):
        return self.index(self.__indexMap.index(sourceIndex), 0)
            
    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if self.__sourceModel is None:
            return QtCore.QVariant()
        
        mIndex = self.modelIndex(index)
        row = mIndex.row()
        parent = mIndex.parent()
        
        return self.__sourceModel.data(self.__sourceModel.index(row, 0, parent), role)

    def flags(self, index):
        if self.__sourceModel is None or not index.isValid():  
            return QtCore.Qt.NoItemFlags
        flags = self.__sourceModel.flags(self.modelIndex(index))
        #Strip all writable flags and make sure we can select it
        return (flags & ~(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsUserCheckable)) | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        
    def hasChildren(self, index):
        return False

    def index(self, row, column, parent = QtCore.QModelIndex()):
        if self.hasIndex(row, column, parent):
            return self.createIndex(row, column)
        return QtCore.QModelIndex()

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, parent):
        return len(self.__indexMap)

    def modelIndex(self, proxyIndex):
        if proxyIndex.isValid():
            row = proxyIndex.row()
            if row < len(self.__indexMap):
                return self.__indexMap[row]
        return QtCore.QModelIndex()
    
    #=========================================
    # source model handler
    #=========================================
    def on_sourceModel_dataChanged(self, topLeft, bottomRight):
        #Cambiaron los datos tengo que ponerlos en funcion del comparableValue
        if topLeft in self.__indexMap:
            self.beginRemoveRows(QtCore.QModelIndex(), self.__indexMap.index(topLeft), self.__indexMap.index(topLeft))
            self.__indexMap.remove(topLeft)
            self.endRemoveRows()
            position = bisect_key(self.__indexMap, topLeft, lambda index: self.comparableValue(index))
            self.beginInsertRows(QtCore.QModelIndex(), position, position)
            self.__indexMap.insert(position, topLeft)
            self.endInsertRows()
            #self.dataChanged.emit(self.mapFromSource(topLeft), self.mapFromSource(topLeft))
    
    def on_sourceModel_rowsInserted(self, parent, start, end):
        for i in xrange(start, end + 1):
            sIndex = self.__sourceModel.index(i, 0, parent)
            if self.filterAcceptsRow(i, parent):
                position = bisect_key(self.__indexMap, sIndex, lambda index: self.comparableValue(index))
                self.beginInsertRows(QtCore.QModelIndex(), position, position)
                self.__indexMap.insert(position, sIndex)
                self.endInsertRows()
    
    def on_sourceModel_rowsAboutToBeRemoved(self, parent, start, end):
        #Remove indexes
        for i in xrange(start, end + 1):
            sIndex = self.sourceModel().index(i, 0, parent)
            if sIndex in self.__indexMap:
                self.beginRemoveRows(QtCore.QModelIndex(), self.__indexMap.index(sIndex), self.__indexMap.index(sIndex))
                self.__indexMap.remove(sIndex)
                self.endRemoveRows()

    def on_sourceModel_layoutChanged(self):
        print "cambio el layout"