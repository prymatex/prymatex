#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore

class TreeNode(object):
    def __init__(self, nodeName, parentNode = None):
        self.name = nodeName
        self.parentNode = parentNode
        self.childrenNodes = []
    
    def isRootNode(self):
        return self.parentNode == None
    
    def appendChild(self, child):
        self.childrenNodes.append(child)
        child.parentNode = self

    def insertChild(self, index, child):
        self.childrenNodes.insert(index, child)
        child.parentNode = self

    def removeChild(self, child):
        self.childrenNodes.remove(child)
        child.parentNode = None
    
    def findChildByName(self, name):
        for child in self.childrenNodes:
            if child.name == name:
                return child

    def removeAllChild(self):
        for child in self.childrenNodes:
            child.parentNode = None
        self.childrenNodes = []

    def childIndex(self, child):
        return self.childrenNodes.index(child)
        
    def childCount(self):
        return len(self.childrenNodes)

    def child(self, row):
        if row < len(self.childrenNodes):
            return self.childrenNodes[row]
    
    def row(self):
        return self.parentNode.childIndex(self)
        
class TreeModel(QtCore.QAbstractItemModel):  
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.rootNode = TreeNode("Root")

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
        parentNode = node.parentNode
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
        
class NodeAlreadyExistsException(Exception):
    pass

class NamespaceTreeModel(TreeModel):  
    def __init__(self, separator = ".", parent = None):
        TreeModel.__init__(self, parent)
        self.separator = separator
        self.__proxyNodeFactory = None
        
    @property
    def proxyNodeFactory(self):
        return self.__proxyNodeFactory
        
    @proxyNodeFactory.setter
    def proxyNodeFactory(self, value):
        self.__proxyNodeFactory = value

    def createProxyNode(self, name, parent):
        if self.proxyNodeFactory is not None:
            proxy = self.proxyNodeFactory(name, parent)
        proxy = TreeNode(name, parent)
        proxy._isproxy = True
        return proxy
        
    def nodeForNamespace(self, namespace, createProxy = False):
        node = self.rootNode
        names = namespace.split(self.separator)
        for name in names:
            if name != "":
                nextNode = node.findChildByName(name)
                if nextNode is None and createProxy:
                    nextNode = self.createProxyNode(name, node)
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
        proxy = parentNode.findChildByName(node.name)
        if proxy != None:
            if proxy._isproxy:
                #Reparent
                for child in proxy.childrenNodes:
                    node.appendChild(child)
                parentNode.removeChild(proxy)
                self.layoutChanged.emit()
            else:
                raise NodeAlreadyExistsException()
        self.beginInsertRows(parentIndex, node.childCount(), node.childCount())
        parentNode.appendChild(node)
        node._isproxy = False
        self.endInsertRows()