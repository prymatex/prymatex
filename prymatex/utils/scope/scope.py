#!/usr/bin/env python
# encoding: utf-8

from parser import Parser


class Scope(object):
    def __init__(self, scope):
        self.path = scope and Parser.path(scope) or Parser.path("")


    def __str__(self):
        return str(self.path)


    def has_prefix(self, rhs):
        lhsScopes = self.path.scopes
        rhsScopes = rhs.path.scopes
        i = 0
        for i in xrange(min(len(lhsScopes), len(rhsScopes))):
            if lhsScopes[i] != rhsScopes[i]:
                break
        return i == len(rhsScopes)

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
        self.left = isinstance(left, Scope) and left or Scope(left)
        self.right = isinstance(right, Scope) and right or Scope(right)

    @classmethod
    def get(cls, left, right = None):
        # TODO: Testing cache
        right = right or left
        if left not in cls.CONTEXTS or right not in cls.CONTEXTS[left]:
            leftCache = cls.CONTEXTS.setdefault(left, {})
            leftCache[right] = cls(left, right)
        return cls.CONTEXTS[left][right]
            
        
    def __str__(self):
        if self.left == self.right:
            return "(l/r '%s')" % str(self.left)
        else:
            "(left '%s', right '%s')" % (str(self.left), str(self.right))
            
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
        return str(self.selector)


    # ------- Matching 
    def does_match(self, context, rank = None):
        if not self.selector:
            if rank is not None:
                rank.append(0)
            return True
        if isinstance(context, (basestring, Scope)):
            context = Context.get(context)
        # TODO: Testing cache
        if context in self.previousMatch:
            rank.append(self.previousMatch[context][1])
            return self.previousMatch[context][0]
        if isinstance(context, Context):
            match = context.left == wildcard or context.right == wildcard or self.selector.does_match(context.left.path, context.right.path, rank)
            self.previousMatch[context] = (match, sum(rank))
            return match