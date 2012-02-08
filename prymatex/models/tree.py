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