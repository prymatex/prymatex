#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.support import processor

class PMXSyntaxProcessor(processor.PMXSyntaxProcessor):
    def __init__(self, editor):
        self.editor = editor

    #START
    def startParsing(self, scope):
        self.setScopes([ scope ])
    
    #BEGIN NEW LINE
    def beginLine(self, line):
        self.line = line
        self.lineIndex = 0
        self.scopeRanges = []       #[ ((start, end), scopeHash) ... ]
        self.lineChunks = []        #[ ((start, end), chunk) ... ]
        
    def endLine(self, line):
        print "end", self.lineIndex, self.stackScopes
        self.addToken(len(self.line) + 1)

    #OPEN
    def openTag(self, scope, position):
        print "open", self.lineIndex, position, self.stackScopes, scope
        self.addToken(position)
        self.stackScopes.append(scope)

    #CLOSE
    def closeTag(self, scope, position):
        print "close", self.lineIndex, position, self.stackScopes, scope
        self.addToken(position)
        self.stackScopes.pop()
    
    #END
    def endParsing(self, scope):
        pass
    
    def setScopes(self, scopes):
        self.stackScopes = scopes

    def scopes(self):
        return self.stackScopes
        
    def addToken(self, end):
        begin = self.lineIndex
        # Solo si tengo realmente algo que agregar
        if begin != end:
            scopeHash = self.editor.flyweightScopeFactory(self.stackScopes)
            self.scopeRanges.append( ((begin, end), scopeHash) )
            self.lineChunks.append( ((begin, end), self.line[begin:end]) )
        self.lineIndex = end

class CodeEditorSyntaxProcessor(processor.PMXSyntaxProcessor):
    def __init__(self, editor):
        self.editor = editor
        self.__scopePath = []
        self.__scopePosition = []
        self.__scopeRanges = {}
        self.__lineChunks = []
    
    def cmp(self, s1, s2):
        v = cmp(s1[0], s2[0])
        if v == 0:
            v = cmp(s2[1], s1[1])
            if v == 0:
                v = cmp(len(self.__scopeRanges[s1]), len(self.__scopeRanges[s2]))
        return v
        
    # Public api
    def scopeRanges(self):
        # Return [ ((start, end), scopeHash) ... ]
        keys = self.__scopeRanges.keys()
        keys.sort(cmp = self.cmp)
        #print map(lambda key: (key, self.__scopeRanges[key]), keys)
        # TODO Analizar mejor la utilidad de esto, quiza dejar los nombres en listas sea mejor
        return map(lambda key: (key, self.editor.flyweightScopeFactory(self.__scopeRanges[key])), keys)
        
    def lineChunks(self):
        return self.__lineChunks
        
    def setScopes(self, path):
        self.__scopePath = path

    def scopes(self):
        return self.__scopePath
    
    #START
    def startParsing(self, scope):
        self.setScopes([ scope ])
    
    #BEGIN NEW LINE
    def beginLine(self, line):
        self.line = line
        self.__scopePosition = [0 for _ in range(len(self.__scopePath))]
        self.__scopeRanges = {}
        self.__lineChunks = []        #[ ((start, end), chunk) ... ]
        
    def endLine(self, line):
        begin = 0
        end = len(self.line) + 1
        path = self.__scopePath[:]
        path.reverse()
        self.__scopeRanges[(begin, end)] = path
        self.__lineChunks.insert(0, ((begin, end), self.line[begin:end]) )

    #OPEN
    def openTag(self, scope, position):
        #print "open", self.__scopePath, scope, position
        self.__scopePath.insert(0, scope)
        self.__scopePosition.insert(0, position)
        
    #CLOSE
    def closeTag(self, scope, position):
        #print "close", self.__scopePath, scope, position
        index = self.__scopePath.index(scope)
        begin = self.__scopePosition[index]
        path = self.__scopePath[index:]
        path.reverse()
        self.__scopeRanges[(begin, position)] = path
        # TODO Ver que pasa con esto de los lineChunks
        self.__lineChunks.insert(0, ((begin, position), self.line[begin:position]) )
        self.__scopePath.pop(index)
        self.__scopePosition.pop(index)
    
    #END
    def endParsing(self, scope):
        pass
