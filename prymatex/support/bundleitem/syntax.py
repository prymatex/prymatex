#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from prymatex.utils import six

from .base import PMXBundleItem
from ..regexp import compileRegexp

class PMXSyntaxProxy(object):
    def __init__(self, dataHash, syntax):
        self.syntax = syntax
        self.proxy = dataHash['include']
    
    def __getattr__(self, name):
        if self.proxy:
            proxy_value = self.__proxy()
            if proxy_value:
                return getattr(proxy_value, name)
    
    def __proxy(self):
        if self.proxy.startswith('#'):
            grammar = self.syntax.grammar
            if hasattr(grammar, 'repository') and self.proxy[1:] in grammar.repository:  
                return grammar.repository[self.proxy[1:]]
        elif self.proxy == '$self':
            return self.syntax.grammar
        elif self.proxy == '$base':
            return self.syntax.grammar
        else:
            syntaxes = self.syntax.syntaxes
            if self.proxy in syntaxes:
                return syntaxes[self.proxy].grammar
            else:
                return PMXSyntaxNode({}, self.syntax)

class PMXSyntaxNode(object):
    KEYS = ('name', 'match', 'begin', 'content', 'contentName', 'end',
            'captures', 'beginCaptures', 'endCaptures', 'repository', 'patterns')
    def __init__(self, dataHash, syntax):
        self.syntax = syntax
        for key in PMXSyntaxNode.KEYS:
            value = dataHash.get(key, None)
            if value is not None:
                if key in ('match', 'begin'):
                    value = compileRegexp( value )
                elif key in ('captures', 'beginCaptures', 'endCaptures'):
                    value = sorted(value.items(), key = lambda v: int(v[0]))
                elif key == 'repository':
                    value = self.parse_repository(value)
                elif key == 'patterns':
                    value = self.create_children(value)
            setattr(self, key, value )
        
        if self.name is not None:
            # Inject
            for injector in self.syntax.injectors.values():
                if injector.injectionSelector.does_match(self.name):
                    if self.patterns is None:
                        self.patterns = []
                    self.patterns.extend(injector.grammar.patterns)

    def parse_repository(self, repository):
        return dict([ (key, 'include' in value and\
                    PMXSyntaxProxy( value, self.syntax ) or\
                    PMXSyntaxNode( value, self.syntax ))
                for key, value in repository.items() ])

    def create_children(self, patterns):
        return [ 'include' in pattern and\
                    PMXSyntaxProxy( pattern, self.syntax ) or\
                    PMXSyntaxNode( pattern, self.syntax )
                for pattern in patterns ]
    
    def parse_captures(self, name, pattern, match, processor):
        captures = pattern.match_captures( name, match )
        #Aca tengo que comparar con -1, Ver nota en match_captures
        captures = [group_range_name for group_range_name in captures if group_range_name[1][0] != -1 and group_range_name[1][0] != group_range_name[1][-1]]
        starts = []
        ends = []
        for group, range, name in captures:
            starts.append((range[0], group, name))
            ends.append((range[-1], -group, name))
        starts = starts[::-1]
        ends = ends[::-1]
        
        while starts or ends:
            if not starts:
                pos, _, name = ends.pop()
                processor.closeTag(name, pos)
            elif not ends:
                pos, _, name = starts.pop()
                processor.openTag(name, pos)
            elif abs(ends[-1][1]) < starts[-1][1]:
                pos, _, name = ends.pop()
                processor.closeTag(name, pos)
            else:
                pos, _, name = starts.pop()
                processor.openTag(name, pos)
    
    def match_captures(self, name, match):
        matches = []
        captures = getattr(self, name)
        
        if captures:
            for key, value in captures:
                if key.isdigit():
                    # TODO 0 es igual a lo capturado no hace falta hacer el match.groups() seria directemente el pattern
                    index = int(key)
                    if index <= len(match.groups()):
                        #Problemas entre python y ruby, al pones un span del match, en un None oniguruma me retorna (-1, -1),
                        #esto es importante para el filtro del llamador
                        matches.append([index, match.span(index), value['name']])
                else:
                    if match.groups()[ key ]:
                        matches.append([match.groups()[ key ], match.groupdict[ key ], value['name']])
        return matches
      
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
        def g_match(mobj):
            index = int(mobj.group(0)[1:])
            return match.group(index)
        def d_match(mobj):
            print("d_match")
            index = mobj.group(0)
            return match.groupdict[index]
        regstring = compileRegexp('\\\\([1-9])').sub(g_match, regstring)
        regstring = compileRegexp('\\\\k<(.*?)>').sub(d_match, regstring)
        return compileRegexp( regstring ).search( string, position )
    
    def match_first_son(self, string, position):
        match = (None, None)
        for p in self.patterns:
            tmatch = p.match_first(string, position)
            if tmatch[1]:
                if not match[1] or match[1].start() > tmatch[1].start():
                    match = tmatch
                #if tmatch[1].start() == position:
                #    break
        return match

class PMXSyntax(PMXBundleItem):
    KEYS = ( 'comment', 'firstLineMatch', 'scopeName', 'repository',
        'fileTypes', 'patterns', 'injectionSelector')
    TYPE = 'syntax'
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
    ROOT_GROUPS = [ "comment", "constant", "entity", "invalid",
                    "keyword", "markup", "meta", "storage",
                    "string", "support", "variable" ]
    
    def load(self, dataHash):
        super(PMXSyntax, self).load(dataHash)
        for key in PMXSyntax.KEYS:
            value = dataHash.get(key, None)
            if value is not None:
                if key == 'firstLineMatch':
                    value = compileRegexp( value )
                elif key == 'scopeName':
                    self.scopeNameSelector = self.manager.createScopeSelector(value)
                elif key == 'injectionSelector':
                    value = self.manager.createScopeSelector(value)
            setattr(self, key, value)
    
    def dump(self, includeNone = False):
        dataHash = super(PMXSyntax, self).dump(includeNone)
        for key in PMXSyntax.KEYS:
            value = getattr(self, key, None)
            if value is not None:
                if key == 'firstLineMatch':
                    value = value.pattern
                elif key == 'injectionSelector':
                    value = six.text_type(value)
                dataHash[key] = value
        return dataHash

    def update(self, dataHash):
        PMXBundleItem.update(self, dataHash)
        if hasattr(self, '_grammar'):
            delattr(self, '_grammar')

    @property
    def syntaxes(self):
        return self.manager.getSyntaxesAsDictionary()

    @property
    def injectors(self):
        return dict(filter(lambda key_val: key_val[1].injectionSelector is not None, 
                self.syntaxes.items()))
    
    @property
    def grammar(self):
        if not hasattr(self, '_grammar'):
            dataHash = {}
            dataHash['repository'] = self.buildRepository() if self.scopeName else {}
            dataHash['patterns'] = self.patterns if self.patterns else []
            self._grammar = PMXSyntaxNode(dataHash , self )
        return self._grammar

    def buildRepository(self):
        repository = {}
        for key, value in self.syntaxes.items():
            if value.scopeNameSelector.does_match(self.scopeName) and\
            value.repository:
                print("Agregando", key)
                repository.update(value.repository)
        return repository

    def parse(self, string, processor = None):
        if processor:
            processor.startParsing(self.scopeName)
        stack = [( self.grammar, None )]
        for line in string.splitlines(True):
            self.parseLine(stack, line, processor)
        if processor:
            processor.endParsing(self.scopeName)
    
    def parseLine(self, stack, line, processor):
        if processor:
            processor.beginLine(line)
        top, match = stack[-1]
        position = 0
        grammar = self.grammar
        
        while True:
            end_match = pattern = pattern_match = None
            if top.patterns:
                pattern, pattern_match = top.match_first_son(line, position)
            if top.end:
                end_match = top.match_end( line, match, position )
            if end_match and ( not pattern_match or pattern_match.start() >= end_match.start() ):
                start_pos = end_match.start()
                end_pos = end_match.end()
                if top.contentName and processor:
                    processor.closeTag(top.contentName, start_pos)
                if processor:
                    grammar.parse_captures('captures', top, end_match, processor)
                if processor:
                    grammar.parse_captures('endCaptures', top, end_match, processor)
                if top.name and processor:
                    processor.closeTag( top.name, end_pos)
                stack.pop()
                top, match = stack[-1]
            elif pattern:
                start_pos = pattern_match.start()
                end_pos = pattern_match.end()
                if pattern.begin:
                    if pattern.name and processor:
                        processor.openTag(pattern.name, start_pos)
                    if processor:
                        grammar.parse_captures('captures', pattern, pattern_match, processor)
                    if processor:
                        grammar.parse_captures('beginCaptures', pattern, pattern_match, processor)
                    if pattern.contentName and processor:
                        processor.openTag(pattern.contentName, end_pos)
                    top = pattern
                    match = pattern_match
                    stack.append((top, match))
                elif pattern.match:
                    if pattern.name and processor:
                        processor.openTag(pattern.name, start_pos)
                    if processor:
                        grammar.parse_captures('captures', pattern, pattern_match, processor)
                    if pattern.name and processor:
                        processor.closeTag(pattern.name, end_pos)
            else:
                # FIXME: Custom pop from stack for regexp
                if not end_match and not pattern and top.end == "(?!\G)":
                    stack.pop()
                break
            position = end_pos
        if processor:
            processor.endLine(line)
        return position

    @classmethod
    def findGroup(cls, scopes):
        for scope in scopes:
            group = scope.split(".")[0]
            if group in cls.ROOT_GROUPS:
                return group
