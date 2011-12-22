#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtCore

class TreeNode(object):
    def __init__(self, name, parent = None):
        self.name = name
        self.parent = parent
        self.children = []
    
    def appendChild(self, child):
        self.children.append(child)
        child.parent = self

    def insertChild(self, index, child):
        self.children.insert(index, child)
        child.parent = self

    def removeChild(self, child):
        self.children.remove(child)
        child.parent = None

    def removeAllChild(self):
        for child in self.children:
            child.parent = None
        self.children = []

    def childIndex(self, child):
        return self.children.index(child)
        
    def childCount(self):
        return len(self.children)

    def child(self, row):
        if row < len(self.children):
            return self.children[row]
    
    def row(self):
        return self.parent.childIndex(self)
        
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
        parentNode = node.parent
        if parentNode == self.rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)
    
    def node(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.rootNode