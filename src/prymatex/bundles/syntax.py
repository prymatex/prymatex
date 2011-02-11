#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Syntax's module
    http://manual.macromates.com/en/language_grammars.html
    http://manual.macromates.com/en/navigation_overview#customizing_foldings.html
'''

import ponyguruma as onig
from ponyguruma.constants import OPTION_CAPTURE_GROUP
from prymatex.bundles.base import PMXBundleItem
from prymatex.bundles.score import PMXScoreManager

onig_compile = onig.Regexp.factory(flags = OPTION_CAPTURE_GROUP)

class PMXSyntaxNode(object):
    def __init__(self, hash, syntax):
        for k in [  'syntax', 'match', 'begin', 'content', 'name', 'contentName', 'end',
                    'captures', 'beginCaptures', 'endCaptures', 'repository', 'patterns']:
            setattr(self, k, None)
        self.syntax = syntax
        for key, value in hash.iteritems():
            if key in ['match', 'begin']:
                setattr(self, key, onig_compile( value ))
            elif key in ['content', 'name', 'contentName', 'end']:
                setattr(self, key, value )
            elif key in ['captures', 'beginCaptures', 'endCaptures']:
                value = sorted(value.items(), key=lambda v: int(v[0]))
                setattr(self, key, value)
            elif key == 'repository':
                self.parse_repository(value)
            elif key in ['patterns']:
                self.create_children(value)
            else:
                print u'%s ignoring %s: %s' % (self.__class__.__name__, key, value)
    
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
        captures = filter(lambda (group, range, name): range[0] and range[0] != range[-1], captures)
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
                processor.open_tag(name, pos)
            elif ends:
                pos, _, name = ends.pop()
                processor.close_tag(name, pos)
            elif abs(ends[-1][1]) < starts[-1][1]:
                pos, _, name = ends.pop()
                processor.close_tag(name, pos)
            else:
                pos, _, name = starts.pop()
                processor.open_tag(name, pos)
    
    def match_captures(self, name, match):
        matches = []
        captures = getattr(self, name)
        
        if captures:
            for key, value in captures:
                if onig_compile('^\d*$').match(key):
                    if int(key) <= len(match.groups):
                        matches.append([int(key), match.span(int(key)), value['name']])
                else:
                    if match.groups[ key ]:
                        matches.append([match.groups[ key ], match.groupdict[ key ], value['name']])
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
        regstring = onig_compile('\\\\([1-9])').sub(g_match, regstring)
        regstring = onig_compile('\\\\k<(.*?)>').sub(d_match, regstring)
        return onig_compile( regstring ).search( string, position )
    
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
        #TODO: else raise exception
    
    def __proxy(self):
        if onig_compile('^#').match(self.proxy):
            grammar = self.syntax.grammar
            if hasattr(grammar, 'repository') and grammar.repository.has_key(self.proxy[1:]):  
                return grammar.repository[self.proxy[1:]]
        elif self.proxy == '$self':
            return self.syntax.grammar
        elif self.proxy == '$base':
            return self.syntax.grammar
        else:
            return self.syntax.syntaxes[self.proxy].grammar
        
class PMXSyntax(PMXBundleItem):
    SYNTAXES = {}
    def __init__(self, hash, name_space = 'default'):
        super(PMXSyntax, self).__init__(hash, name_space)
        for key in [    'comment', 'firstLineMatch', 'foldingStartMarker', 'scopeName', 'repository',
                        'keyEquivalent', 'foldingStopMarker', 'fileTypes', 'patterns']:
            value = hash.pop(key, None)
            if value != None and key in ['firstLineMatch', 'foldingStartMarker', 'foldingStopMarker']:
                #Compiled keys
                value = onig_compile( value )
            setattr(self, key, value)

        if hash:
            print "Syntax '%s' has more values (%s)" % (self.name, ', '.join(hash.keys()))
            
        PMXSyntax.SYNTAXES.setdefault(self.name_space, {})
        if self.scopeName != None:
            PMXSyntax.SYNTAXES[self.name_space][self.scopeName] = self

    @property
    def syntaxes(self):
        return PMXSyntax.SYNTAXES[self.name_space]

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
            processor.start_parsing(self.scopeName)
        stack = [[self.grammar, None]]
        for line in string.splitlines():
            self.parse_line(stack, line, processor)
        if processor:
            processor.end_parsing(self.scopeName)
        return stack

    def parse_line(self, stack, line, processor):
        if processor:
            processor.new_line(line)
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
                    processor.close_tag(top.contentName, start_pos)
                if processor:
                    grammar.parse_captures('captures', top, pattern_match, processor)
                if processor:
                    grammar.parse_captures('endCaptures', top, pattern_match, processor)
                if top.name and processor:
                    processor.close_tag( top.name, end_pos)
                stack.pop()
                top, match = stack[-1]
            else:
                if not pattern:
                    break 
                start_pos = pattern_match.start()
                end_pos = pattern_match.end()
                if pattern.begin:
                    if pattern.name and processor:
                        processor.open_tag(pattern.name, start_pos)
                    if processor:    
                        grammar.parse_captures('captures', pattern, pattern_match, processor)
                    if processor:
                        grammar.parse_captures('beginCaptures', pattern, pattern_match, processor)
                    if pattern.contentName and processor:
                        processor.open_tag(pattern.contentName, end_pos)
                    top = pattern
                    match = pattern_match
                    stack.append([top, match])
                elif pattern.match:
                    if pattern.name and processor:
                        processor.open_tag(pattern.name, start_pos)
                    if processor:
                        grammar.parse_captures('captures', pattern, pattern_match, processor)
                    if pattern.name and processor:
                        processor.close_tag(pattern.name, end_pos)
            position = end_pos
        return position
        
    @classmethod
    def findSyntaxByFirstLine(cls, line):
        for _, syntaxes in cls.SYNTAXES.iteritems():
            for _, syntax in syntaxes.iteritems():
                if syntax.firstLineMatch != None and syntax.firstLineMatch.match(line):
                    return syntax
    
    @classmethod
    def findSyntaxByFileType(cls, path):
        for _, syntaxes in cls.SYNTAXES.iteritems():
            for _, syntax in syntaxes.iteritems():
                if type(syntax.fileTypes) == list:
                    for t in syntax.fileTypes:
                        if path.endswith(t):
                            return syntax
                
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
    def getSyntaxesByScope(cls, scope):
        stxs = []
        scores = PMXScoreManager()
        for _, syntaxes in cls.SYNTAXES.iteritems():
            for _, syntax in syntaxes.iteritems():
                score = scores.score(scope, syntax.scopeName)
                if score != 0:
                    stxs.append((score, syntax))
        stxs.sort(key = lambda t: t[0])
        return map(lambda (score, stx): stx, stxs)
    
    @classmethod
    def getSyntaxesNames(cls, sort = False):
        stxs = []
        for _, syntaxes in cls.SYNTAXES.iteritems():
            for _, syntax in syntaxes.iteritems():
                stxs.append(syntax.name)
        if sort:
            return sorted(stxs)
        return stxs
                
def parse_file(filename):
    import plistlib
    from pprint import pprint
    data = plistlib.readPlist(filename)
    pprint(data)
    return PMXSyntax(data)

if __name__ == '__main__':
    import os
    from glob import glob
    files = glob(os.path.join('../share/Bundles/Bundle Development.tmbundle/Syntaxes', '*'))
    for f in files:
        syntax = parse_file(f)
    print PMXSyntax.SYNTAXES