#!/usr/bin/env python
from __future__ import unicode_literals

from .parser import parse_snippet
from . import types

def collect(nodes, placeholders):
    for node in filter(lambda node: isinstance(node, (types.PlaceholderType, types.PlaceholderChoiceType)), nodes):
        if node.index not in placeholders:
            placeholders[node.index] = node
    for node in filter(lambda node: isinstance(node, types.PlaceholderType), nodes):
        collect(node.content, placeholders)

class Snippet(object):
    LAST_INDEX = "0"
    def __init__(self, source):
        self.nodes = parse_snippet(source)
        self.placeholders = {}
        collect(self.nodes, self.placeholders)
        self.__hasLastHolder = self.LAST_INDEX in self.placeholders
        if not self.__hasLastHolder:
            self.placeholders[self.LAST_INDEX] = types.PlaceholderType(self.LAST_INDEX)
            self.nodes.append(self.placeholders[self.LAST_INDEX])

    def __str__(self):
        return "".join([unicode(node) for node in self.lastHolderFixed() and self.nodes[:-1] or self.nodes ])
    
    __unicode__ = __str__
    
    def lastHolderFixed(self):
        return not self.__hasLastHolder

    def replace(self, memodict):
        return "".join([node.replace(memodict, holders = self.placeholders) for node in self.nodes])

    def render(self, visitor, memodict):
        for node in self.nodes:
            node.render(visitor, memodict, holders = self.placeholders)

    def __len__(self):
        return len(self.placeholders)
    
    # TODO: Add parameter for partial resolution
    # $PATH:$HOME/Scripts if environement has not PATH then dont resolve 
    def substitute(self, variables = {}):
        v = Visitor(variables)
        self.render(v, types.Memodict())
        return v.output
        
class Visitor(object):
    def __init__(self, variables = {}):
        self.output = ""
        self.variables = variables

    def startRender(self):
        self.output = ""

    def endRender(self):
        pass
        
    def insertText(self, text):
        self.output += text 

    def caretPosition(self):
        return len(self.output)
        
    def environmentVariables(self):
        return self.variables

class SnippetHandler(object):
    def __init__(self):
        self.snippet = None
        self.holders = None
        self.taborder = None
        self.holderIndex = None
        self.memodict = None
        
    def hasSnippet(self):
        return self.snippet is not None

    def setSnippet(self, snippet):
        self.snippet = snippet
        self.taborder = sorted(snippet.placeholders.keys())
        self.taborder.append(self.taborder.pop(0))
        self.holders = [ snippet.placeholders[key] for key in self.taborder ]

    def reset(self):
        self.memodict = types.Memodict()
        self.holderIndex = 0

    def render(self, visitor):
        assert self.snippet is not None
        visitor.beginRender()
        self.snippet.render(visitor, self.memodict)
        visitor.endRender()

    def __current_holder(self):
        return self.holders[self.holderIndex]
        
    def __is_disabled(self, holder):
        placeholders = filter(
            lambda node: isinstance(node, types.PlaceholderType), 
            self.holders)
        for placeholder in placeholders:
            chain = [ ]
            if placeholder.collect(holder, chain):
                return any(map(lambda holder: self.memodict.get_or_create(holder).content is not None, chain))
        return False
        
    def currentPosition(self):
        return self.__current_holder().position(self.memodict)

    def setHolder(self, start, end = None):
        '''Set the placeholder for position, where start > holder position > end'''
        end = end is not None and end or start
        found = None
        for holder in self.holders:
            holderStart, holderEnd = holder.position(self.memodict)
            holderLength = holderEnd - holderStart
            if holderStart <= start <= end <= holderEnd and \
                (found is None or holderLength < found):
                found = holderLength
                self.holderIndex = self.holders.index(holder)
        return found is not None

    def nextHolder(self):
        if self.holderIndex < len(self.holders) - 1:
            self.holderIndex += 1
            #Fix disabled placeholders
            while self.holderIndex < len(self.holders) - 1 and self.__is_disabled(self.holders[self.holderIndex]):
                self.holderIndex += 1
            return True
        return False

    def previousHolder(self):
        if self.holderIndex > 0:
            self.holderIndex -= 1
            #Fix disabled placeholders
            while self.holderIndex != 0 and self.__is_disabled(self.holders[self.holderIndex]):
                self.holderIndex -= 1
            return True
        return False

    def lastHolder(self):
        # Si el snippet esta fixeado tons last holder son dos el utimo y el fix
        index = self.taborder.index(self.__current_holder().index)
        if self.snippet.lastHolderFixed():
            index += 1
        return index + 1 >= len(self.taborder) 

    def holderNumber(self):
        return self.holderIndex + 1

    def setHolderContent(self, text):
        self.__current_holder().setContent(text, self.memodict)

    def hasHolderContent(self):
        return self.__current_holder().hasContent(self.memodict)
    
    def lastHolderFixed(self):
        return self.snippet.lastHolderFixed()

    def holderChoices(self):
        return getattr(self.__current_holder(), "choices", [])
        
    def __len__(self):
        return len(self.snippet)
