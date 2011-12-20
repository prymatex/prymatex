#!/usr/bin/env python
#-*- encoding: utf-8 -*-

class TreeNode(object):
    def __init__(self, name, parent = None):
        self.name = name
        self.parent = parent
        self.children = []
    
    def appendChild(self, child):
        self.children.append(child)
        child.parent = self

    def removeChild(self, child):
        self.children.remove(child)
        child.parent = None

    def childIndex(self, child):
        return self.children.index(child)
        
    def childCount(self):
        return len(self.children)

    def child(self, row):
        if row < len(self.children):
            return self.children[row]
    
    def row(self):
        return self.parent.childIndex(self)