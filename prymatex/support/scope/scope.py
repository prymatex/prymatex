#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from prymatex.utils import six

from .parser import Parser
from .types import PathType, ScopeType

class Scope(object):
    def __init__(self, path = None):
        self.path = isinstance(path, PathType) and path or Parser.path(path)

    @classmethod
    def fast_build(cls, path):
        path = path.split() if isinstance(path, six.string_types) else path
        return cls(PathType([ ScopeType(p.split(".")) for p in path ]))

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
    CONTEXTS = {}
    def __init__(self, left, right):
        self.left = isinstance(left, Scope) and left or Scope.fast_build(left)
        self.right = isinstance(right, Scope) and right or Scope.fast_build(right)

    @classmethod
    def get(cls, left, right = None):
        right = right or left
        if left not in cls.CONTEXTS or right not in cls.CONTEXTS[left]:
            leftCache = cls.CONTEXTS.setdefault(left, {})
            leftCache[right] = cls(left, right)
        return cls.CONTEXTS[left][right]
        
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
        self.previousMatch = {}

    def __str__(self):
        return six.text_type(self.selector)

    # ------- Matching 
    def does_match(self, context, rank = None):
        #assert isinstance(rank, list)
        if not self.selector:
            if rank is not None:
                rank.append(0)
            return True

        if isinstance(context, (tuple, six.string_types, Scope)):
            context = Context.get(context)

        # Search in cache
        matchKey = (context, isinstance(rank, list))
        if matchKey in self.previousMatch:
            if matchKey[1]:
                rank.append(self.previousMatch[matchKey][1])
            return self.previousMatch[matchKey][0]
        
        match = context.left == wildcard or context.right == wildcard or self.selector.does_match(context.left.path, context.right.path, rank)
        self.previousMatch[matchKey] = (match, matchKey[1] and sum(rank) or None)
        return match
