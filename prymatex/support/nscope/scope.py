#!/usr/bin/env python

import sys

from .parser import Parser

ROOTS = ( "comment", "constant", "entity", "invalid", "keyword", "markup",
"meta", "storage", "string", "support", "variable" )            

class Scope(object):
    class Node(tuple):
        def __new__(cls, iter, parent):
            return super(Scope.Node, cls).__new__(cls, iter)

        def __init__(self, iter, parent):
            self.parent = parent

        def is_auxiliary_scope(self):
            return self[0] in ("attr", "dyn")

        def number_of_atoms(self):
    	        return len(self)
        
    def __init__(self, source = None):
        self.node = None
        if isinstance(source, Scope.Node):
            # From node
            self.node = source
        elif isinstance(source, Scope):
            # By clone
            self.node = source.node
        elif source:
            # From source string
            for atom in source.split():
                self.push_scope(atom)

    @classmethod
    def factory(cls, source):
        return cls(source)

    def __hash__(self):
        return hash("%s" % self)

    def __eq__(self, rhs):
        n1, n2 = self.node, rhs.node
        while n1 and n2 and n1 == n2:
            n1 = n1.parent
            n2 = n2.parent
        return n1 is None and n2 is None

    def __ne__(self, rhs):
        return not self == rhs

    def __bool__(self):
        return not self.empty()

    def __str__(self):
        res = []
        n = self.node
        while n is not None:
            res.append(".".join(n))
            n = n.parent
        return " ".join(res[::-1])
    
    # --------- Python 2
    __nonzero__ = __bool__
    __unicode__ = __str__

    def clone(self):
        return Scope(self)

    def empty(self):
        return self.node is None

    def push_scope(self, atom):
        self.node = Scope.Node(atom.split("."), self.node)
    
    def pop_scope(self):
        assert(self.node is not None)
        self.node = self.node.parent

    def back(self):
        assert(self.node is not None)
        return ".".join(self.node)

    def size(self):
        res = 0
        n = self.node
        while n is not None:
            res += 1
            n = n.parent
        return res

    def has_prefix(self, rhs):
        lhs = Scope(self)
        rhs = Scope(rhs)
        lhsSize, rhsSize = lhs.size(), rhs.size()
        for _ in range(lhsSize - rhsSize):
            lhs.pop_scope()
        return lhs == rhs
    
    def rootGroupName(self):
        node = self.node
        while node is not None:
            for atom in node.split("."):
                if atom in ROOTS:
                    return atom
                node = node.parent

wildcard = Scope("x-any")

def shared_prefix(lhs, rhs):
    return ""

def xml_difference(frm, to, open = "<", close = ">"):
    return ""

class Context(object):
    def __init__(self, left = None, right = None):
        self.left = Scope(left)
        self.right = right is not None and Scope(right) or Scope(left)
        
    def __eq__(self, rhs):
        return self.left == rhs.left and self.right == rhs.right
    
    def __ne__(self, rhs):
        return not self == rhs
    
    def __lt__(self, rhs):
        return self.left < rhs.left or self.left == self.rhs.left and self.right < rhs.right

    def __str__(self):
        if self.left == self.right:
            return "(l/r '%s')" % self.left
        else:
            return "(left '%s', right '%s')" % (self.left, self.right)

    # --------- Python 2
    __unicode__ = __str__
    
class Selector(object):
    def __init__(self, source = None):
        self._selector = None
        if source is not None:
            self._selector = Parser.selector(source)

    def __repr__(self):
        return repr(self._selector)
        
    def __str__(self):
        return self._selector and "%s" % self._selector or ""

    # --------- Python 2
    __unicode__ = __str__
    
    # ------- Matching 
    def does_match(self, context, rank = None):
        if not isinstance(context, Context):
            context = Context(context)
        if self._selector:
            return context.left == wildcard or context.right == wildcard or self._selector.does_match(context.left, context.right, rank)
        if rank is not None:        
            rank.append(0)
        return True
