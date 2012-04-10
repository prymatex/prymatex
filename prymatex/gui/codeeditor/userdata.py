#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy
from PyQt4 import QtGui
from prymatex.support.syntax import PMXSyntax

class PMXBlockUserData(QtGui.QTextBlockUserData):
    def __init__(self):
        QtGui.QTextBlockUserData.__init__(self)
        self.scopes = []
        #Folding
        self.foldingMark = None
        self.foldedLevel = 0
        self.folded = False
        #Indent
        self.indent = ""
        #Symbols
        self.symbol = None
        #Words
        self.words = []

        self.textHash = None
        self.cache = None

    def __nonzero__(self):
        return bool(self.scopes)
    
    def getLastScope(self):
        return self.scopes[-1]
    
    def setScopes(self, scopes):
        self.scopes = scopes
        
    def getScopeAtPosition(self, pos):
        #FIXME: Voy a poner algo mentiroso si pos no esta en self.scopes
        scope = self.scopes[pos] if pos < len(self.scopes) else self.scopes[-1]
        return scope
    
    def scopeRange(self, pos):
        ranges = self.scopeRanges()
        range = filter(lambda (scope, start, end): start <= pos <= end, ranges)
        assert len(range) >= 1, "More than one range"
        range = range[0] if len(range) == 1 else None
        return range
    
    def scopeRanges(self, start = 0, end = None):
        current = ( self.scopes[start], start ) if start < len(self.scopes) else ("", 0)
        end = end or len(self.scopes)
        scopes = []
        for index, scope in enumerate(self.scopes[start:], start):
            if scope != current[0]:
                scopes.append(( current[0], current[1], index ))
                current = ( scope, index )
        scopes.append(( current[0], current[1], end ))
        return scopes
    
    def isWordInScopes(self, word):
        return word in reduce(lambda scope, scope1: scope + " " + scope1[0], self.scopeRanges(), "")

    #http://manual.macromates.com/en/language_grammars
    def entities(self):
        """entity — an entity refers to a larger part of the document, for example a chapter, class, function, or tag.
        We do not scope the entire entity as entity.* (we use meta.* for that). But we do use entity.* for the “placeholders”
        in the larger entity, e.g. if the entity is a chapter, we would use entity.name.section for the chapter title.
            name — we are naming the larger entity.
                function — the name of a function.
                type — the name of a type declaration or class.
                tag — a tag name.
                section — the name is the name of a section/heading.
            other — other entities.
                inherited-class — the superclass/baseclass name.
                attribute-name — the name of an attribute (mainly in tags).
        """
        return filter(lambda scope: 'entity' in scope[0], self.scopeRanges())

    #================================================
    # Cache Handle
    #================================================
    def getStackAndScopes(self):
        return copy(self.cache[0]), copy(self.cache[1])
    
    def setStackAndScopes(self, stack, scopes):
        self.cache = (stack, scopes)