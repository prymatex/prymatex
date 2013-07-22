#!/usr/bin/env python
from __future__ import unicode_literals

from .parser import parse_snippet
from . import types

def collect(nodes, placeholders):
    for node in nodes:
        if isinstance(node, (types.PlaceholderType, types.PlaceholderChoiceType)):
            if node.index not in placeholders:
                placeholders[node.index] = node
            if isinstance(node, types.PlaceholderType):
                collect(node.content, placeholders)

class Snippet(object):
    def __init__(self, source):
        self.nodes = parse_snippet(source)
        self.placeholders = {}
        collect(self.nodes, self.placeholders)
        self.__hasLastHolder = '0' in self.placeholders
        if not self.__hasLastHolder:
            self.placeholders['0'] = types.PlaceholderType("0")
            self.nodes.append(self.placeholders['0'])

    def __str__(self):
        return "".join([unicode(node) for node in self.__hasLastHolder and self.nodes or self.nodes[:-1]])
    
    __unicode__ = __str__
    
    def replace(self, memodict):
        return "".join([node.replace(memodict, holders = self.placeholders) for node in self.nodes])

    def render(self, visitor, memodict):
        for node in self.nodes:
            node.render(visitor, memodict, holders = self.placeholders)

class Visitor(object):
    def __init__(self):
        self.output = ""
        self.variables = {}

    def resetOutput(self):
        self.output = ""

    def insertText(self, text):
        self.output += text 

    def position(self):
        return len(self.output)
        
    def environmentVariables(self):
        return self.variables

class SnippetHandler(object):
    def __init__(self):
        self.snippet = None
        self.placeholders = [ ]

    def setSnippet(self, snippet):
        self.snippet = snippet
        taborder = sorted(snippet.placeholders.keys())
        taborder.append(taborder.pop(0))
        self.placeholders = [ snippet.placeholders[key] for key in taborder ]

    def execute(self, visitor):
        self.memodict = types.Memodict()
        self.holderIndex = 0
        self.render(visitor)

    def render(self, visitor):
        assert self.snippet is not None
        visitor.resetOutput()
        self.snippet.render(visitor, self.memodict)

    def __is_disabled(self, holder):
        placeholders = filter(
            lambda node: isinstance(node, types.PlaceholderType), 
            self.placeholders)
        for placeholder in placeholders:
            chain = []
            if placeholder.collect(holder, chain):
                return any(map(lambda holder: self.memodict.get_or_create(holder).content, chain))
        return False
        
    def setHolder(self, start, end = None):
        '''Set the placeholder for position, where start > holder position > end'''
        end = end != None and end or start
        found = None
        for holder in self.placeholders:
            holderStart, holderEnd = holder.position(self.memodict)
            holderLength = holderEnd -holderStart
            if holderStart <= start <= end <= holderEnd and \
                (found == None or holderLength < found):
                found = holderLength
                self.holderIndex = self.placeholders.index(holder)
        return found != None

    def nextHolder(self):
        if self.holderIndex < len(self.placeholders) - 1:
            self.holderIndex += 1
            #Fix disabled placeholders
            while self.holderIndex < len(self.placeholders) - 1 and self.__is_disabled(self.placeholders[self.holderIndex]):
                self.holderIndex += 1
            return True
        return False

    def previousHolder(self):
        if self.holderIndex > 0:
            self.holderIndex -= 1
            #Fix disabled placeholders
            while self.holderIndex != 0 and self.__is_disabled(self.placeholders[self.holderIndex]):
                self.holderIndex -= 1
            return True
        return False

    def lastHolder(self):
        return self.holderIndex == len(self.placeholders)

    def setContent(self, text):
        self.placeholders[self.holderIndex].setContent(text, self.memodict)
