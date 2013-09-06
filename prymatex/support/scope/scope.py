#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from prymatex.utils import six

from .parser import Parser
from .types import PathType, ScopeType

class Scope(object):
    def __init__(self, path):
        self.path = isinstance(path, PathType) and path or Parser.path(path)

    @classmethod
    def factory(cls, path):
        return cls(PathType(tuple([ ScopeType(tuple(p.split("."))) for p in path ])))
    
    def __str__(self):
        return six.text_type(self.path)

    def has_prefix(self, rhs):
        lhsScopes = self.path.scopes
        rhsScopes = rhs.path.scopes
        i = 0
        for i in range(min(len(lhsScopes), len(rhsScopes))):
            if lhsScopes[i] != rhsScopes[i]:
                break
        return i == len(rhsScopes)

    def __hash__(self):
        return hash(self.path)
      
    def __eq__(self, rhs):
        return self.path == rhs.path
    
    def __ne__(self, rhs):
        return not self == rhs
    
    def __lt__(self, rhs):
        return self.path < self.rhs.path
        
    def __bool__(self, rhs):
        return bool(self.path)

wildcard = Scope("x-any")

class Context(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        if self.left == self.right:
            return "(l/r '%s')" % six.text_type(self.left)
        else:
            return "(left '%s', right '%s')" % (six.text_type(self.left), six.text_type(self.right))
    
    def __hash__(self):
        return hash(six.text_type(self.left)) + hash(six.text_type(self.right))

    def __eq__(self, rhs):
        return self.left == rhs.left and self.right == rhs.right
    
    def __ne__(self, rhs):
        return not self == rhs
    
    def __lt__(self, rhs):
        return self.left < rhs.left or self.left == self.rhs.left and self.right < rhs.right

class Selector(object):
    def __init__(self, selector):
        self.selector = selector and Parser.selector(selector)
        
    def __str__(self):
        return six.text_type(self.selector)

    # ------- Matching 
    def does_match(self, context, rank = None):
        #assert isinstance(rank, list)
        if not self.selector:
            if rank is not None:
                rank.append(0)
            return True
        
        if isinstance(context, Scope):
            context = Context(context, context)
        
        match = context.left == wildcard or context.right == wildcard or self.selector.does_match(context.left.path, context.right.path, rank)
        return match
