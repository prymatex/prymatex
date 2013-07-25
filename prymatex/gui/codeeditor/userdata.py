#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from prymatex.qt import QtGui

from functools import reduce

CodeEditorBlockUserDataToken = namedtuple("CodeEditorBlockUserDataToken", [
    "start", "end", "scopeHash", "chunk"
])

class CodeEditorBlockUserData(QtGui.QTextBlockUserData):

    def __init__(self):
        QtGui.QTextBlockUserData.__init__(self)
        self.__stateHash = None
        
        self.__blank = True
        self.__tokens = []
        
        self.__scopeRanges = None
        self.__lineChunks = None
        self.__cache = {}

    def setStateHash(self, stateHash):
        self.__stateHash = stateHash

    def testStateHash(self, stateHash):
        return self.__stateHash == stateHash

    def setTokens(self, tokens):
        self.__tokens = tokens
        self.__scopeRanges = None
        self.__lineChunks = None

    def tokens(self, start = None, end = None):
        tokens = self.__tokens
        if start is not None:
            tokens = [ token for token in tokens if token.start >= start ]
        if end is not None:
            tokens = [ token for token in tokens if token.end <= end ]
        return tokens

    def scopeRanges(self, start = None, end = None):
        # deprecated
        if not self.__scopeRanges:
            self.__scopeRanges = [ ((token.start, token.end), token.scopeHash) for token in self.__tokens ]
        ranges = self.__scopeRanges[:]
        if start is not None:
            ranges = [ range for range in ranges if range[0][0] >= start ]
        if end is not None:
            ranges = [ range for range in ranges if range[0][1] <= end ]
        return ranges

    def lineChunks(self):
        # deprecated
        if not self.__lineChunks:
            self.__lineChunks = [ ((token.start, token.end), token.chunk) for token in self.__tokens ]
        return self.__lineChunks[:]

    def setBlank(self, blank):
        self.__blank = blank
    
    def blank(self):
        return self.__blank
        
    def lastToken(self):
        return self.__tokens[-1]
    
    def tokenAtPosition(self, pos):
        for token in self.__tokens[::-1]:
            if token.start <= pos <= token.end:
                return token

    # ------------------- Cache Handle
    def processorState(self):
        return self.__cache.get("processor_state", ([], []))

    def setProcessorState(self, processorState):
        self.__cache["processor_state"] = processorState

    def saveState(self):
        return {}
        
    def restoreState(self, state):
        pass
