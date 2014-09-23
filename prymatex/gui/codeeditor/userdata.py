#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from prymatex.qt import QtGui
from prymatex.support import Scope

class CodeEditorToken(namedtuple('CodeEditorToken', 'start end scope chunk')):
        __slots__ = ()
        @property
        def group(self):
            return self.scope.rootGroupName()

_empty_token = CodeEditorToken(0,0,Scope(),"")

class CodeEditorBlockUserData(QtGui.QTextBlockUserData):

    def __init__(self):
        QtGui.QTextBlockUserData.__init__(self)
        
        self.__blank = True
        self.__tokens = []
        self.__ranges = None
        self.__revision = None

        self.__cache = {}

    def setRevision(self, revision):
        self.__revision = revision

    def revision(self):
        return self.__revision
                
    def setTokens(self, tokens):
        self.__tokens = tokens
        self.__ranges = None

    def tokens(self, start = None, end = None):
        tokens = self.__tokens
        if start is not None:
            tokens = [ token for token in tokens if token.start >= start ]
        if end is not None:
            tokens = [ token for token in tokens if token.end <= end ]
        return tokens

    def ranges(self, start = None, end = None):
        if self.__ranges is None:
            ranges = set()
            for token in self.tokens(start, end):
                ranges.add(token.start)
                ranges.add(token.end)
            self.__ranges = sorted(ranges)
        return self.__ranges
    
    def setBlank(self, blank):
        self.__blank = blank
    
    def blank(self):
        return self.__blank
        
    def lastToken(self):
        return self.__tokens and self.__tokens[-1] or _empty_token
    
    def tokenAtPosition(self, pos):
        for token in self.__tokens[::-1]:
            if token.start <= pos < token.end:
                return token
        return _empty_token

    # ------------------- Cache Handle
    def processorState(self):
        return self.__cache.get("processor_state", ([], Scope()))

    def setProcessorState(self, processorState):
        self.__cache["processor_state"] = processorState

    def saveState(self):
        return {}
        
    def restoreState(self, state):
        pass
