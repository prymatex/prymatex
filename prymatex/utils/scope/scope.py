#!/usr/bin/env python
# encoding: utf-8

from parser import Parser


class Scope(object):
    def __init__(self, scope):
        self.path = Parser.path(scope)


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


wildcard = Scope("x-any")


class Selector(object):
    def __init__(self, selector = None):
        self.selector = Parser.selector(selector) if selector else selector


    def __str__(self):
        return str(self.selector)


    # ------- Matching 
    def does_match(self, scope, rank = None):
        if isinstance(scope, basestring):
            scope = Scope(scope)
        if not self.selector:
            if rank is not None:
                rank.append(0)
            return True
        if not scope.path:
            return False
        return scope == wildcard or self.selector.does_match(scope.path, scope.path, rank)
