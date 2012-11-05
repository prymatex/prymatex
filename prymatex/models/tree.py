#!/usr/bin/env python
#-*- encoding: utf-8 -*-

"""
OLD TREE MODULE, USE TREES
"""

from prymatex.qt import QtCore

from prymatex.utils.lists import bisect_key

class TreeNode(object):
    def __init__(self, nodeName, nodeParent = None):
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
    
    def childNodes(self):
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

    def removeAllChild(self):
        self.__children = []

    def popChild(self, index = -1):
        return self.__children.pop(index)
        
    def childIndex(self, child):
        return self.__children.index(child)
        
    def childCount(self):
        return len(self.__children)

    def child(self, row):
        if row < len(self.__children):
            return self.__children[row]
    
    def row(self):
        return self.__nodeParent.childIndex(self)
        
    def column(self):
        return 0

class TreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.rootNode = self.treeNodeFactory("root", None)

    def treeNodeFactory(self, nodeName, nodeParent):
        return TreeNode(nodeName, nodeParent)

    def rowCount(self, parentIndex):
        return self.node(parentIndex).childCount()
        
    def columnCount(self, parentIndex):
        return 1

    def index(self, row, column, parentIndex):
        parentNode = self.node(parentIndex)
        childNode = parentNode.child(row)
        if childNode is not None:
            return self.createIndex(row, column, childNode)
        else:
            return QtCore.QModelIndex()
    
    def parent(self, index):
        node = self.node(index)
        parentNode = node.nodeParent()
        # Todo ver si puede llegar como index el root porque algo en este if no esta bien
        if parentNode is None or parentNode.isRootNode():
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), parentNode.column(), parentNode)
    
    def nodeIndex(self, node):
        if not node.isRootNode():
            return self.createIndex(node.row(), node.column(), node)
        else:
            return QtCore.QModelIndex()
    
    def node(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.rootNode
    
    def clear(self):
        self.rootNode.removeAllChild()
        self.layoutChanged.emit()
    
    def appendNode(self, node, parentNode = None):
        # TODO: validar y retornar falso si no se puede, ver si el parent puede ser index y node
        parentNode = parentNode or self.rootNode
        parentIndex = self.nodeIndex(parentNode)
        self.beginInsertRows(parentIndex, parentNode.childCount(), parentNode.childCount())
        parentNode.appendChild(node)
        self.endInsertRows()
        return True
        
    def removeNode(self, node, parentNode = None):
        # TODO: validar y retornar falso si no se puede, ver si el parent puede ser index y node
        parentNode = parentNode or self.rootNode
        parentIndex = self.nodeIndex(parentNode)
        self.beginRemoveRows(parentIndex, node.row(), node.row())
        parentNode.removeChild(node)
        self.endRemoveRows()
        return True
        
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
    
    def insertNode(self, node):
        # TODO esto es como un appendNode asi que no estaria mal que se use ese metodo
        return self.addNamespaceNode("", node)

    def insertNamespaceNode(self, namespace, node):
        parentNode = self.nodeForNamespace(namespace, True)
        parentIndex = self.nodeIndex(parentNode)
        #Check if exit proxy for setting
        proxy = parentNode.findChildByName(node.nodeName())
        if proxy != None:
            if proxy._isproxy:
                #Reparent
                for child in proxy.childNodes():
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
        node = self.__sourceModel.node(sIndex)
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
        
        sIndex = self.mapToSource(index)
        
        return self.__sourceModel.data(sIndex, role)

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