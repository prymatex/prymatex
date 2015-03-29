#!/usr/bin/env python

import sys

from .parser import Parser

ROOTS = ( "comment", "constant", "entity", "invalid", "keyword", "markup",
"meta", "storage", "string", "support", "variable" )            

class Scope(object):
    class Node(tuple):
        def __new__(cls, iterable, parent):
            return super(Scope.Node, cls).__new__(cls, iterable)

        def __init__(self, iter, parent):
            self.parent = parent
            self._hash = None

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
        return " ".join([".".join(n) for n in self])
    
    def __iter__(self):
        res = []
        n = self.node
        while n is not None:
            res.append(n)
            n = n.parent
        return iter(res[::-1])

    def __add__(self, other):
        new = self.clone()
        new.extend(other)
        return new

    # --------- Python 2
    __nonzero__ = __bool__
    __unicode__ = __str__

    def clone(self):
        return Scope(self)
    
    def extend(self, other):
        [self.push(n) for n in other]

    def empty(self):
        return self.node is None

    def push(self, iterable):
        self.node = Scope.Node(iterable, self.node)

    def pop(self):
        assert(self.node is not None)
        node = self.node
        self.node = self.node.parent
        return node

    def push_scope(self, atom):
        self.push(atom.split("."))
    
    def pop_scope(self):
        return ".".join(self.pop())

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
    
    def root_group(self):
        best = node = self.node
        while node is not None:
            if node[0] in ROOTS:
                best = node
            node = node.parent
        return best
    
    @staticmethod
    def shared_prefix(lhs, rhs):
        lhsSize, rhsSize = lhs.size(), rhs.size()
        n1, n2 = lhs.node, rhs.node
        for i in range(rhsSize, lhsSize):
            n1 = n1.parent
        for i in range(lhsSize, rhsSize):
            n2 = n2.parent
    
        while n1 and n2 and n1 == n2:
            n1 = n1.parent
            n2 = n2.parent
        
        return Scope(n1)
    
    @staticmethod
    def xml_difference(frm, to, open_string = "<", close_string = ">"):
        fromScopes, toScopes = [], []
        tmp = Scope(frm)
        while not tmp.empty():
            fromScopes.append(tmp.back())
            tmp.pop_scope()
        tmp = Scope(to)
        while not tmp.empty():
            toScopes.append(tmp.back())
            tmp.pop_scope()
        
        fromIter, toIter = len(fromScopes) - 1, len(toScopes) - 1
        while fromIter != -1 and toIter != -1 and fromScopes[fromIter] == toScopes[toIter]:
            fromIter -= 1
            toIter -= 1
        
        res = ""
        for it in range(fromIter + 1):
            res += (open_string + "/" + fromScopes[it] + close_string)
    
        while toIter != -1:
            res += (open_string + toScopes[toIter] + close_string)
            toIter -= 1
    
        return res
    
wildcard = Scope("x-any")

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

    def __bool__(self):
        return self._selector is not None
        
    def __repr__(self):
        return repr(self._selector)
        
    def __str__(self):
        return self._selector and "%s" % self._selector or ""

    # --------- Python 2
    __nonzero__ = __bool__
    __unicode__ = __str__
    
    # ------- Matching 
    def does_match(self, context, rank = None):
        if not isinstance(context, Context):
            context = Context(context)
        if self:
            return context.left == wildcard or context.right == wildcard or self._selector.does_match(context.left, context.right, rank)
        if rank is not None:        
            rank.append(0)
        return True
