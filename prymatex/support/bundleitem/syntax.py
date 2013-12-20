#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from functools import reduce
import types

from prymatex.utils import six

from .base import BundleItem
from ..regexp import compileRegexp, String

# ==========================
# = Node syntax definition =
# ==========================
class SyntaxNode(object):
    KEYS = ('name', 'contentName', 'match', 'begin', 'content', 'end',
            'captures', 'beginCaptures', 'endCaptures', 'repository', 'patterns')
    def __init__(self, dataHash, parentNode = None):
        self.parentNode = parentNode
        for key in SyntaxNode.KEYS:
            value = dataHash.get(key, None)
            if value is not None and key in ('match', 'begin'):
                value = compileRegexp( value )
            elif value is not None and key in ('captures', 'beginCaptures', 'endCaptures'):
                value = dict(
                    map(lambda item: (item[0], SyntaxNode(item[1], self)), value.items())
                )
            elif key == 'repository':
                value = self.parse_repository(value or {})
            elif key == 'patterns':
                value = self.create_children(value or [])
            setattr(self, key, value )
        
        if self.name is not None:
            # String for name
            self._nameFormater = String(self.name)
            
        if self.contentName is not None:
            # String for contentName
            self._contentNameFormater = String(self.contentName)
    
    def inject(self, injectors, scopeFactoryFunction):
        for pattern in filter(lambda p: isinstance(p, SyntaxNode), self.patterns):
            pattern.inject(injectors, scopeFactoryFunction)
        if self.name:
            scope = scopeFactoryFunction(self.name)
            for injector in injectors:
                if injector.injectionSelector.does_match(scope):
                    self.patterns.extend(self.create_children(injector.patterns or []))
                    self.repository.update(self.parse_repository(injector.repository or {}))

    def parse_repository(self, repository):
        return dict([ (key, 'include' in value and\
                    SyntaxProxyNode( value["include"], self ) or\
                    SyntaxNode( value, self ))
                for key, value in repository.items() ])

    def create_children(self, patterns):
        return [ 'include' in pattern and\
                    SyntaxProxyNode( pattern["include"], self ) or\
                    SyntaxNode( pattern, self )
                for pattern in patterns ]
    
    def parse_captures(self, name, pattern, match, processor):
        #Aca tengo que comparar con -1, Ver nota en match_captures
        captures = filter(lambda capture: 
            capture[1][0] != -1 and capture[1][0] != capture[1][-1],
            pattern.match_captures( name, match ))
        
        close = []
        for group, _range, value in sorted(captures, key = lambda t: t[0]):
            if close and close[-1][1] <= _range[0]:
                processor.closeTag(close[-1][0], close[-1][1])
                close.pop()
            if value.name:
                _ex_name = value._nameFormater.expand(match)
                processor.openTag(_ex_name, _range[0])
                close.append((_ex_name, _range[1]))
            else:
                stack = [(value, None)]
                value.parse_source(_range[0], stack, match.group(group), processor)
        while close:
            processor.closeTag(close[-1][0], close[-1][1])
            close.pop()

    def match_captures(self, name, match):
        captures = getattr(self, name) or {}
        len_groups = len(match.groups())
        for key, value in captures.items():
            if key.isdigit():
                index = int(key)
                if index <= len_groups:
                    yield ( index, match.span(index), value )
            else:
                yield ( match.groups().index(match.group(key)), match.span(key), value )

    def match_first(self, string, position):
        if self.match:
            match = self.match.search( string, position )
            if match:
                return (self, match)
        elif self.begin:
            match = self.begin.search( string, position )
            if match:
                return (self, match)
        elif self.end:
            pass
        elif self.patterns:
            return self.match_first_son( string, position )
        return (None, None)
    
    def match_end(self, string, match, position):
        regstring = self.end[:]
        def d_match(mobj):
            print("d_match")
            index = mobj.group(0)
            return match.groupdict[index]
        regstring = compileRegexp('\\\\([1-9])').sub(
            lambda mobj: match.group(int(mobj.group(0)[1:])),
            regstring)
        regstring = compileRegexp('\\\\k<(.*?)>').sub(d_match, regstring)
        regexp = compileRegexp( regstring )
        if regexp:
            return regexp.search( string, position )
    
    def match_first_son(self, string, position):
        son = match = None
        for p in self.patterns:
            tson, tmatch = p.match_first(string, position)
            if tmatch:
                if tmatch.start() == 0:
                    son, match = tson, tmatch
                    break
                if not match or match.start() > tmatch.start():
                    son, match = tson, tmatch

        # Expand names
        if son and (son.name or son.contentName):
            if son.name:
                son._ex_name = son._nameFormater.expand(match)
            if son.contentName:
                son._ex_contentName = son._contentNameFormater.expand(match)
        return (son, match)

    def parse(self, text, processor):
        processor.beginParse(self.scopeName)
        stack = [( self, None )]
        for line in text.splitlines(True):
            self.parse_line(stack, line, processor)
        processor.endParse(self.scopeName)
    
    def parse_line(self, stack, line, processor):
        processor.beginLine(line)
        position = self.parse_source(0, stack, line, processor)
        processor.endLine(line)
    
    def parse_source(self, position, stack, source, processor):
        top, match = stack[-1]
        
        while True:
            end_match = pattern = pattern_match = None
            if top.patterns:
                pattern, pattern_match = top.match_first_son(source, position)
            if top.end:
                end_match = top.match_end( source, match, position )
            if end_match and ( not pattern_match or pattern_match.start() >= end_match.start() ):
                start_pos = end_match.start()
                end_pos = end_match.end()
                if top.contentName:
                    processor.closeTag(top._ex_contentName, start_pos)
                self.parse_captures('captures', top, end_match, processor)
                self.parse_captures('endCaptures', top, end_match, processor)
                if top.name:
                    processor.closeTag( top._ex_name, end_pos)
                stack.pop()
                top, match = stack[-1]
            else:
                if not pattern:
                    break

                start_pos = pattern_match.start()
                end_pos = pattern_match.end()
                if pattern.begin:
                    if pattern.name:
                        processor.openTag(pattern._ex_name, start_pos)
                    self.parse_captures('captures', pattern, pattern_match, processor)
                    self.parse_captures('beginCaptures', pattern, pattern_match, processor)
                    if pattern.contentName:
                        processor.openTag(pattern._ex_contentName, end_pos)
                    top = pattern
                    match = pattern_match
                    stack.append((top, match))
                elif pattern.match:
                    if pattern.name:
                        processor.openTag(pattern._ex_name, start_pos)
                    self.parse_captures('captures', pattern, pattern_match, processor)
                    if pattern.name:
                        processor.closeTag(pattern._ex_name, end_pos)
            position = end_pos
            
        # Fixed stack
        if stack and stack[-1][0].name is None and stack[-1][0].contentName is None:
            stack.pop()
        return position

# ================
# = Syntax proxy =
# ================
class SyntaxProxyNode(object):
    def __init__(self, proxyName, parentNode):
        self.parentNode = parentNode
        self.__proxyName = proxyName
        self.__proxyValue = None
        self.__rootNode = None

    def __getattr__(self, name):
        if self.__proxyValue is None:
            self.__proxyValue = self.__proxy()
        return getattr(self.__proxyValue, name)
    
    @property
    def rootNode(self):
        if self.__rootNode is None:
            self.__rootNode = self
            while self.__rootNode.parentNode:
                self.__rootNode = self.__rootNode.parentNode
        return self.__rootNode
        
    def __proxy(self):
        if self.__proxyName.startswith('#'):
            name = self.__proxyName[1:]
            repository = getattr(self.rootNode, 'repository')
            if name in repository:
                return repository[name]
            parentNode = self.parentNode
            while parentNode:
                repository = getattr(parentNode, 'repository')
                if name in repository:
                    return repository[name]
                parentNode = parentNode.parentNode
        elif self.__proxyName in ['$self', '$base']:
            return self.rootNode
        else:
            return self.rootNode.findSyntax(self.__proxyName)
        
class Syntax(BundleItem):
    KEYS = ( 'comment', 'firstLineMatch', 'scopeName', 'repository',
        'fileTypes', 'patterns', 'injectionSelector')
    FOLDER = 'Syntaxes'
    EXTENSION = 'tmLanguage'
    PATTERNS = ('*.tmLanguage', '*.plist')
    DEFAULTS = {
        'name': 'untitled',
        'scopeName': 'source.untitled',
        'fileTypes': [],
        'foldingStartMarker': '/\*\*|\{\s*$',
        'foldingStopMarker': '\*\*/|^\s*\}',
        'patterns': [ 
            { 
                'name': 'keyword.control.untitled',
                'match': '\b(if|while|for|return)\b' 
            },
            {
                'name': 'string.quoted.double.untitled',
                'begin': '"',
                'end': '"',
                'patterns': [
                    { 
                        'name': 'constant.character.escape.untitled',
                        'match': '\\.'
                    }
            ]}
        ],
        'repository': []
    }

    def load(self, dataHash):
        super(Syntax, self).load(dataHash)
        for key in Syntax.KEYS:
            value = dataHash.get(key, None)
            if value is not None:
                if key == 'firstLineMatch':
                    value = compileRegexp( value )
                elif key == 'injectionSelector':
                    value = self.manager.selectorFactory(value)
                elif key == 'scopeName':
                    self.scopeNameSelector = self.manager.selectorFactory(value)
            setattr(self, key, value)
    
    def dump(self, allKeys = False):
        dataHash = super(Syntax, self).dump(allKeys)
        for key in Syntax.KEYS:
            value = getattr(self, key, None)
            if value is not None:
                if key == 'firstLineMatch':
                    value = value.pattern
                elif key == 'injectionSelector':
                    value = six.text_type(value)
                dataHash[key] = value
        return dataHash

    def update(self, dataHash):
        BundleItem.update(self, dataHash)
        if hasattr(self, '_grammar'):
            delattr(self, '_grammar')
    
    @property
    def grammar(self):
        if not hasattr(self, '_grammar'):
            # Build grammar
            
            dataHash = {
                'repository': self.repository,
                'name': self.scopeName,
                'patterns': self.patterns
            }
            self._grammar = SyntaxNode(dataHash)

            # Syntaxes
            def findSyntax(item):
                def _findSyntax(self, scopeName):
                    scope = item.manager.scopeFactory(scopeName)
                    syntaxes = item.manager.getSyntaxesByScope(scope)
                    if syntaxes:
                        return syntaxes[0].grammar
                    return SyntaxNode({})
                return _findSyntax
            self._grammar.findSyntax = types.MethodType(findSyntax(self), self._grammar)
            self._grammar.inject([injector for injector in self.manager.getAllSyntaxes() if 
                         injector.injectionSelector ], self.manager.scopeFactory)
        return self._grammar

    def execute(self, processor):
        processor.beginExecution(self)
        if not processor.managed():
            self.parse(processor.plainText(), processor)
            processor.endExecution(self)

    def parse(self, text, processor):
        self.grammar.parse(text, processor)
    
    def parseLine(self, stack, line, processor):
        self.grammar.parse_line(stack, line, processor)
