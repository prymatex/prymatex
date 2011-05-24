#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Syntax's module
    http://manual.macromates.com/en/language_grammars.html
    http://manual.macromates.com/en/navigation_overview#customizing_foldings.html
'''

import re
try:
    from ponyguruma import sre
except Exception, e:
    sre = re
from prymatex.support.bundle import PMXBundleItem

# Profiling

try:
    from prymatex.lib.profilehooks import profile
    from PyQt4.Qt import qApp
except Exception, e:
    PROFILING_CAPABLE = False
else:
    PROFILING_CAPABLE = qApp.instance() != None
    
def compileRegexp(string):
    #Muejejejeje
    try:
        restring = string.replace('?i:', '(?i)')
        return re.compile(unicode(restring))
    except:
        try:
            return sre.compile(unicode(string))
        except:
            #Mala leche
            pass

SPLITLINES = re.compile('\n')

class PMXSyntaxNode(object):
    def __init__(self, hash, syntax):
        for k in [  'syntax', 'match', 'begin', 'content', 'name', 'contentName', 'end',
                    'captures', 'beginCaptures', 'endCaptures', 'repository', 'patterns']:
            setattr(self, k, None)
        self.syntax = syntax
        for key, value in hash.iteritems():
            try:
                if key in ['match', 'begin']:
                    setattr(self, key, compileRegexp( value ))
                elif key in ['content', 'name', 'contentName', 'end']:
                    setattr(self, key, value )
                elif key in ['captures', 'beginCaptures', 'endCaptures']:
                    value = sorted(value.items(), key=lambda v: int(v[0]))
                    setattr(self, key, value)
                elif key == 'repository':
                    self.parse_repository(value)
                elif key in ['patterns']:
                    self.create_children(value)
            except TypeError, e:
                #an encoding can only be given for non-unicode patterns
                print e, value
    
    def parse_repository(self, repository):
        self.repository = {}
        for key, value in repository.iteritems():
            if 'include' in value:
                self.repository[key] = PMXSyntaxProxy( value, self.syntax )
            else:
                self.repository[key] = PMXSyntaxNode( value, self.syntax )

    def create_children(self, patterns):
        self.patterns = []
        for p in patterns:
            if 'include' in p:
                self.patterns.append(PMXSyntaxProxy( p, self.syntax ))
            else:
                self.patterns.append(PMXSyntaxNode( p, self.syntax ))
    
    def parse_captures(self, name, pattern, match, processor):
        captures = pattern.match_captures( name, match )
        #Aca tengo que comparar con -1, Ver nota en match_captures
        captures = filter(lambda (group, range, name): range != -1 and range[0] != range[-1], captures)
        starts = []
        ends = []
        for group, range, name in captures:
            starts.append([range[0], group, name])
            ends.append([range[-1], -group, name])
        starts = starts[::-1]
        ends = ends[::-1]
        
        while starts or ends:
            if starts:
                pos, _, name = starts.pop()
                processor.openTag(name, pos)
            elif ends:
                pos, _, name = ends.pop()
                processor.closeTag(name, pos)
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
                if re.compile('^\d*$').match(key):
                    if int(key) <= len(match.groups()):
                        #Problemas entre pytgon y ruby, al pones un span del match, en un None oniguruma me retorna (-1, -1),
                        #esto es importante para el filtro del llamador
                        matches.append([int(key), match.span(int(key)), value['name']])
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
        else:
            return self.match_first_son( string, position )
        return (None, None)
    
    def match_end(self, string, match, position):
        regstring = self.end[:]
        def g_match(mobj):
            index = int(mobj.group(0)[1:])
            return match.group(index)
        def d_match(mobj):
            print "d_match"
            index = mobj.group(0)
            return match.groupdict[index]
        regstring = compileRegexp(u'\\\\([1-9])').sub(g_match, regstring)
        regstring = compileRegexp(u'\\\\k<(.*?)>').sub(d_match, regstring)
        return compileRegexp( regstring ).search( string, position )
    
    def match_first_son(self, string, position):
        match = (None, None)
        if self.patterns:
            for p in self.patterns:
                tmatch = p.match_first(string, position)
                if tmatch[1]:
                    if not match[1] or match[1].start() > tmatch[1].start():
                        match = tmatch
        return match

class PMXSyntaxProxy(object):
    def __init__(self, hash, syntax):
        self.syntax = syntax
        self.proxy = hash['include']
    
    def __getattr__(self, name):
        if self.proxy:
            proxy_value = self.__proxy()
            if proxy_value:
                return getattr(proxy_value, name)
    
    def __proxy(self):
        if re.compile('^#').search(self.proxy):
            grammar = self.syntax.grammar
            if hasattr(grammar, 'repository') and grammar.repository.has_key(self.proxy[1:]):  
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

class PMXSyntax(PMXBundleItem):
    KEYS = [ 'comment', 'firstLineMatch', 'foldingStartMarker', 'scopeName', 'repository', 'foldingStopMarker', 'fileTypes', 'patterns']
    TYPE = 'syntax'
    FOLDER = 'Syntaxes'
    EXTENSION = 'tmLanguage'
    PATTERNS = ['*.tmLanguage', '*.plist']
    FOLDING_NONE = 0
    FOLDING_START = -1
    FOLDING_STOP = -2
    def __init__(self, namespace, hash = None, path = None):
        super(PMXSyntax, self).__init__(namespace, hash, path)

    def load(self, hash):
        super(PMXSyntax, self).load(hash)
        for key in PMXSyntax.KEYS:
            value = hash.get(key, None)
            if value != None and key in ['firstLineMatch', 'foldingStartMarker', 'foldingStopMarker']:
                try:
                    value = compileRegexp( value )
                except TypeError, e:
                    value = None
                    print self.name, key, e
            setattr(self, key, value)
    
    @property
    def hash(self):
        hash = super(PMXSyntax, self).hash
        for key in PMXSyntax.KEYS:
            value = getattr(self, key)
            if value != None:
                if key in ['firstLineMatch', 'foldingStartMarker', 'foldingStopMarker']:
                    value = unicode(value)
                hash[key] = value
        return hash

    #Deprecated es una chanchada
    @property
    def indentSensitive(self):
        #If stop marker match with "" the grammar is indent sensitive
        return False

    @property
    def syntaxes(self):
        return self.bundle.manager.SYNTAXES

    @property
    def grammar(self):
        if not hasattr(self, '_grammar'):
            hash = {}
            if self.repository != None:
                hash['repository'] = self.repository
            if self.patterns != None:
                hash['patterns'] = self.patterns
            setattr(self, '_grammar', PMXSyntaxNode(hash , self ))
        return self._grammar

        
    def parse(self, string, processor = None):
        if processor:
            processor.startParsing(self.scopeName)
        stack = [[self.grammar, None]]
        for line in SPLITLINES.split(string):
            self.parseLine(stack, line, processor)
        if processor:
            processor.endParsing(self.scopeName)
        return stack
    
    if PROFILING_CAPABLE and qApp.instance().options.profiling:
        parse = profile(parse)

    def parseLine(self, stack, line, processor):
        if processor:
            processor.newLine(line)
        top, match = stack[-1]
        position = 0
        grammar = self.grammar
        
        while True:
            if top.patterns:
                pattern, pattern_match = top.match_first_son(line, position)
            else:
                pattern, pattern_match = None, None
            end_match = None
            if top.end:
                end_match = top.match_end( line, match, position )
            
            if end_match and ( not pattern_match or pattern_match.start() >= end_match.start() ):
                pattern_match = end_match
                start_pos = pattern_match.start()
                end_pos = pattern_match.end()
                if top.contentName and processor:
                    processor.closeTag(top.contentName, start_pos)
                if processor:
                    grammar.parse_captures('captures', top, pattern_match, processor)
                if processor:
                    grammar.parse_captures('endCaptures', top, pattern_match, processor)
                if top.name and processor:
                    processor.closeTag( top.name, end_pos)
                stack.pop()
                top, match = stack[-1]
            else:
                if not pattern:
                    break 
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
                    stack.append([top, match])
                elif pattern.match:
                    if pattern.name and processor:
                        processor.openTag(pattern.name, start_pos)
                    if processor:
                        grammar.parse_captures('captures', pattern, pattern_match, processor)
                    if pattern.name and processor:
                        processor.closeTag(pattern.name, end_pos)
            position = end_pos
        return position
    
    def folding(self, line):
        fold = self.FOLDING_NONE
        start_match = self.foldingStartMarker.search(line) if self.foldingStartMarker != None else None
        stop_match = self.foldingStopMarker.search(line) if self.foldingStopMarker != None else None
        if start_match != None and stop_match == None:
            fold = self.FOLDING_START
        elif stop_match != None and start_match == None:
            fold = self.FOLDING_STOP
        return fold
                
    @classmethod
    def getSyntaxesByName(cls, name):
        stxs = []
        for _, syntaxes in cls.SYNTAXES.iteritems():
            for _, syntax in syntaxes.iteritems():
                if syntax.name == name:
                    stxs.append(syntax)
        return stxs
    
    @classmethod
    def getSyntaxByName(cls, name):
        #TODO: if more than one, throw Exception
        stxs = cls.getSyntaxesByName(name)
        if stxs:
            return stxs[0]
    
    @classmethod
    def getSyntaxByScope(cls, scope):
        for syntaxes in cls.SYNTAXES.values():
            if scope in syntaxes:
                return syntaxes[scope]
        return None
    
    @classmethod
    def getSyntaxesNames(cls, sort = False):
        stxs = []
        for syntaxes in cls.SYNTAXES.values():
            for syntax in syntaxes.values():
                stxs.append(syntax.name)
        if sort:
            return sorted(stxs)
        return stxs
    
    @classmethod
    def getSyntaxesMenuTextEntry(cls, sort = False):
        stxs = []
        for syntaxes in cls.SYNTAXES.values():
            for syntax in syntaxes.values():
                stxs.append(syntax.buildMenuTextEntry())
        if sort:
            return sorted(stxs)
        return stxs
    
    def __str__(self):
        return u"<PMXSyntax %s>" % self.name
        