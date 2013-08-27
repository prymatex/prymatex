#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from prymatex.utils import six

from .base import PMXBundleItem
from ..regexp import compileRegexp, String

# ==========================
# = Node syntax definition =
# ==========================
class SyntaxNode(object):
    KEYS = ('name', 'contentName', 'match', 'begin', 'content', 'end',
            'captures', 'beginCaptures', 'endCaptures', 'repository', 'patterns')
    def __init__(self, dataHash, rootSyntax, parentNode = None):
        self.rootSyntax = rootSyntax
        self.parentNode = parentNode
        for key in SyntaxNode.KEYS:
            value = dataHash.get(key, None)
            if value is not None and key in ('match', 'begin'):
                value = compileRegexp( value )
            elif value is not None and key in ('captures', 'beginCaptures', 'endCaptures'):
                value = dict(
                    map(lambda item: (item[0], SyntaxNode(item[1], self.rootSyntax, self)), value.items())
                )
            elif key == 'repository':
                value = self.parse_repository(value)
            elif key == 'patterns':
                value = self.create_children(value)
            setattr(self, key, value )
        
        if self.name is not None:
            # Inject
            for injector in self.rootSyntax.injectors.values():
                if injector.injectionSelector.does_match(self.name):
                    if self.patterns is None:
                        self.patterns = []
                    self.patterns.extend(injector.grammar.patterns)

            # String for name
            self._nameFormater = "$" in self.name and String(self.name) or None 
        
        if self.contentName is not None:
            # String for contentName
            self._contentNameFormater = "$" in self.contentName and String(self.contentName) or None 

    def parse_repository(self, repository = None):
        if repository is None:
            return {}
        return dict([ (key, 'include' in value and\
                    SyntaxProxyNode( value["include"], self.rootSyntax, self ) or\
                    SyntaxNode( value, self.rootSyntax, self ))
                for key, value in repository.items() ])

    def create_children(self, patterns = None):
        if patterns is None:
            return []
        return [ 'include' in pattern and\
                    SyntaxProxyNode( pattern["include"], self.rootSyntax, self ) or\
                    SyntaxNode( pattern, self.rootSyntax, self )
                for pattern in patterns ]
    
    def parse_captures(self, name, pattern, match, processor):
        #Aca tengo que comparar con -1, Ver nota en match_captures
        captures = filter(lambda capture: 
            capture[1][0] != -1 and capture[1][0] != capture[1][-1],
            pattern.match_captures( name, match ))
        starts = []
        ends = []
        for group, _range, value in captures:
            starts.append((_range[0], group, value))
            ends.append((_range[-1], group, value))
        starts = starts[::-1]
        ends = ends[::-1]
        # Agarrate de algo
        
        def apply_captures(position, group, value, method):
            if value.patterns and method == "openTag":
                stack = [(value, None)]
                print(position, match.group(group))
                value.parse_source(position, stack, match.group(group), processor)
            elif value.name:
                name = value._nameFormater and value._nameFormater.expand(match) or value.name
                getattr(processor, method)(name, position)
            else:
                print("nada", position, group, value, method)
                
        while starts or ends:
            if not starts:
                pos, group, value = ends.pop()
                apply_captures(pos, group, value, "closeTag")
            elif not ends:
                pos, group, value = starts.pop()
                apply_captures(pos, group, value, "openTag")
            elif ends[-1][1] < starts[-1][1]:
                pos, group, value = ends.pop()
                apply_captures(pos, group, value, "closeTag")
            else:
                pos, group, value = starts.pop()
                apply_captures(pos, group, value, "openTag")

    def match_captures(self, name, match):
        matches = []
        captures = getattr(self, name) or {}
        groups_len = len(match.groups())

        for key, value in captures.items():
            if key.isdigit():
                index = int(key)
                if index < groups_len:
                    matches.append(( index, match.span(index), value ))
            else:
                matches.append(( match.groups().index(match.group(key)), match.span(key), value ))
        # TODO Ver si no hay que entregarlos ordenados por (index,,)
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
                if tmatch[1].start() == 0:
                    match = tmatch
                    break
                if not match[1] or match[1].start() > tmatch[1].start():
                    match = tmatch
        # Expand names
        if match[1] is not None and (match[0].name or match[0].contentName):
            if match[0].name:
                match[0]._ex_name = match[0]._nameFormater and match[0]._nameFormater.expand(match[1]) or match[0].name
            if match[0].contentName:
                match[0]._ex_contentName = match[0]._contentNameFormater and match[0]._contentNameFormater.expand(match[1]) or match[0].contentName
        return match

    def parse(self, text, processor = None):
        if processor:
            processor.startParsing(self.scopeName)
        stack = [( self, None )]
        for line in text.splitlines(True):
            self.parse_line(stack, line, processor)
        if processor:
            processor.endParsing(self.scopeName)
    
    def parse_line(self, stack, line, processor):
        if processor:
            processor.beginLine(line)
        position = self.parse_source(0, stack, line, processor)
        if processor:
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
                if top.contentName and processor:
                    processor.closeTag(top._ex_contentName, start_pos)
                if processor:
                    self.parse_captures('captures', top, end_match, processor)
                if processor:
                    self.parse_captures('endCaptures', top, end_match, processor)
                if top.name and processor:
                    processor.closeTag( top._ex_name, end_pos)
                stack.pop()
                top, match = stack[-1]
            else:
                if not pattern:
                    break

                start_pos = pattern_match.start()
                end_pos = pattern_match.end()
                if pattern.begin:
                    if pattern.name and processor:
                        processor.openTag(pattern._ex_name, start_pos)
                    if processor:
                        self.parse_captures('captures', pattern, pattern_match, processor)
                    if processor:
                        self.parse_captures('beginCaptures', pattern, pattern_match, processor)
                    if pattern.contentName and processor:
                        processor.openTag(pattern._ex_contentName, end_pos)
                    top = pattern
                    match = pattern_match
                    stack.append((top, match))
                elif pattern.match:
                    if pattern.name and processor:
                        processor.openTag(pattern._ex_name, start_pos)
                    if processor:
                        self.parse_captures('captures', pattern, pattern_match, processor)
                    if pattern.name and processor:
                        processor.closeTag(pattern._ex_name, end_pos)
            position = end_pos
        return position

# ================
# = Syntax proxy =
# ================
class SyntaxProxyNode(object):
    def __init__(self, proxyName, rootSyntax, parentNode = None):
        self.rootSyntax = rootSyntax
        self.parentNode = parentNode
        self.__proxyName = proxyName
        self.__proxyValue = None
    
    def __getattr__(self, name):
        if self.__proxyValue is None:
            self.__proxyValue = self.__proxy()
        return getattr(self.__proxyValue, name)

    def __proxy(self):
        if self.__proxyName.startswith('#'):
            name = self.__proxyName[1:]
            repository = getattr(self.rootSyntax.grammar, 'repository')
            if name in repository:
                return repository[name]
            parentNode = self.parentNode
            while parentNode:
                repository = getattr(parentNode, 'repository')
                if name in repository:
                    return repository[name]
                parentNode = parentNode.parentNode
        elif self.__proxyName in ['$self', '$base']:
            return self.rootSyntax.grammar
        else:
            syntaxes = self.rootSyntax.syntaxes
            if self.__proxyName in syntaxes:
                return syntaxes[self.__proxyName].grammar
        print("Algo esta mal")
        return SyntaxNode({}, self.rootSyntax)

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
    
    def dump(self, allKeys = False):
        dataHash = super(PMXSyntax, self).dump(allKeys)
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
            self._grammar = SyntaxNode(dataHash, self)
        return self._grammar

    def buildRepository(self):
        repository = {}
        for key, value in self.syntaxes.items():
            if value.scopeNameSelector.does_match(self.scopeName) and\
            value.repository:
                repository.update(value.repository)
        return repository

    def parse(self, text, processor = None):
        self.grammar.parse(text, processor)
    
    def parseLine(self, stack, line, processor):
        self.grammar.parse_line(stack, line, processor)
        
    @classmethod
    def findGroup(cls, scopes):
        for scope in scopes:
            group = scope.split(".")[0]
            if group in cls.ROOT_GROUPS:
                return group
