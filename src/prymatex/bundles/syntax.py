#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Syntax's module
        content, name, scope, keyEquivalent, tabTrigger
'''

import ponyguruma as onig

PMX_SYNTAXES = {}

OPTIONS = onig.OPTION_CAPTURE_GROUP
onig_compile = onig.Regexp.factory(OPTIONS)

######################### SyntaxProcessor #################################

class PMXSyntaxProcessor(object):
    '''
        Syntax Processor, clase base para los procesadores de sintaxis
    '''
    def __init__(self):
        pass

    def open_tag(self, name, position):
        pass

    def close_tag(self, name, position):
        pass

    def new_line(self, line):
        pass

    def start_parsing(self, name):
        pass

    def end_parsing(self, name):
        pass

class PMXDebugSyntaxProcessor(PMXSyntaxProcessor):
    def __init__(self):
        self.line_number = 0
        self.printable_line = ''

    def pprint(self, line, string, position = 0):
        line = line[:position] + string + line[position:]
        return line

    def open_tag(self, name, position):
        print self.pprint( '', '{ %d - %s' % (position, name), position + len(self.line_marks))

    def close_tag(self, name, position):
        print self.pprint( '', '} %d - %s' % (position, name), position + len(self.line_marks))

    def new_line(self, line):
        self.line_number += 1
        self.line_marks = '[%04s] ' % self.line_number
        print '%s%s' % (self.line_marks, line)

    def start_parsing(self, name):
        print '{%s' % name

    def end_parsing(self, name):
        print '}%s' % name

################################## ScoreManager ###################################

class PMXScoreManager(object):
    POINT_DEPTH    = 4
    NESTING_DEPTH  = 40
    START_VALUE    = 2 ** ( POINT_DEPTH * NESTING_DEPTH )
    BASE           = 2 ** POINT_DEPTH
      
    def __init__(self):
        self.scores = {}
    
    def score(self, search_scope, reference_scope):
        maxi = 0
        for scope in search_scope.split( ',' ):
            arrays = onig_compile("\B-").split(scope)
            if len(arrays) == 1:
                maxi = max([maxi, self.score_term( arrays[0], reference_scope )])
            elif len(arrays) > 1:
                excluded = False
                for a in arrays[1:]:
                    if self.score_term( a, reference_scope ) > 0:
                        excluded = True
                        break
                if not excluded:
                    maxi = max([maxi, self.score_term( arrays[0], reference_scope )])
            elif len(arrays) < 1:
                raise Exception("Error in scope string: '%s' %s is not a valid number of operands" % (search_scope, len(arrays)))
        return maxi
    
    def score_term(self, search_scope, reference_scope):
        if not (self.scores.has_key(reference_scope) and self.scores[reference_scope].has_key(search_scope)):
            self.scores.setdefault(reference_scope, {})
            self.scores[reference_scope][search_scope] = self.score_array( search_scope.split(' '), reference_scope.split( ' ' ) )
        return self.scores[reference_scope][search_scope]
      
    def score_array(self, search_array, reference_array):
        pending = search_array
        current = reference_array[-1]
        reg = onig_compile( "^%s" % onig.escape( pending[-1] ))
        multiplier = self.START_VALUE
        result = 0
        while len(pending) > 0 and current:
            match = reg.match(current)
            if match:
                point_score = (2 ** self.POINT_DEPTH) - current.count( '.' ) + match.group().count( '.' )
                result += point_score * multiplier
                pending.pop()
                if len(pending) > 0:
                    reg = onig_compile( "^%s" % onig.escape( pending[-1] ) )
            multiplier = multiplier / self.BASE
            reference_array.pop()
            current = reference_array and reference_array[-1] or None
        if len(pending) > 0:
            result = 0
        return result

############################## Syntax ######################################

class PMXSyntaxNode(object):
    def __init__(self, hash, syntax):
        for k in [  'syntax', 'match', 'begin', 'content', 'name', 'contentName', 'end',
                    'captures', 'beginCaptures', 'endCaptures', 'repository', 'patterns']:
            setattr(self, k, None)
        self.syntax = syntax
        for key, value in hash.iteritems():
            if key in ['match', 'begin']:
                try:
                    # TODO: Estos replace hay que sacarlos si usamos el motor de expreciones de la dll
                    setattr(self, key, onig_compile( value ))
                except:
                    pass
                    #print 'Parsing error in %s - %s:%s' % (self.syntax.scopeName, key, value)
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
                pass
                #print u'Ignoring: %s: %s' % (key, value)
    
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
        
        ''' if key =~ /^\d*$/
                matches << [key.to_i, match.offset( key.to_i ), value["name"]] if key.to_i < match.size
            else
                matches << [match.to_index( key.to_sym ), match.offset( key.to_sym), value["name"]] if match.to_index( key.to_sym )
        '''
        
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
            print "g_match"
            index = mobj.group(0)
            return match.group(index)
        def d_match(mobj):
            print "d_match"
            index = mobj.group(0)
            return match.groupdict[index]
        regstring = onig_compile('\\\\([1-9])').sub(g_match, regstring)
        regstring = onig_compile('\\\\k<(.*?)>').sub(d_match, regstring)
        return onig_compile( regstring ).match( string, position )
    
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
        
class PMXSyntax(object):
    def __init__(self, hash, name_space = 'default'):
        global PMX_SYNTAXES
        self.hash = hash
        self.name_space = name_space
        for key in [    'comment', 'firstLineMatch', 'foldingStartMarker', 'name', 
                        'scopeName', 'keyEquivalent', 'foldingStopMarker', 'fileTypes']:
            value = self.hash.pop(key, None)
            if value != None and key in ['firstLineMatch', 'foldingStartMarker', 'foldingStopMarker']:
                #Compiled keys
                value = onig_compile( value )
            setattr(self, key, value)

        if hash:
            print "Command '%s' has more values (%s)" % (self.name, ', '.join(hash.keys()))
            
        PMX_SYNTAXES.setdefault(self.name_space, {})
        if self.scopeName == None:
            raise Exception("Syntax don't have scopeName")
        PMX_SYNTAXES[self.name_space][self.scopeName] = self

    @property
    def syntaxes(self):
        return PMX_SYNTAXES[self.name_space]

    @property
    def grammar(self):
        if not hasattr(self, '_grammar'):
            setattr(self, '_grammar', PMXSyntaxNode(self.hash, self ))
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
        
def find_syntax_by_first_line(line):
    for _, syntaxes in PMX_SYNTAXES.iteritems():
        for _, syntax in syntaxes.iteritems():
            if syntax.firstLineMatch != None and syntax.firstLineMatch.match(line):
                return syntax

def parse_file(filename):
    import plistlib
    data = plistlib.readPlist(filename)
    return PMXSyntax(data)

if __name__ == '__main__':
    import os
    from glob import glob
    files = glob(os.path.join('../share/Bundles/C.tmbundle/Syntaxes', '*'))
    for f in files:
        syntax = parse_file(f)
    p = PMXDebugSyntaxProcessor()
    print PMX_SYNTAXES
    print PMX_SYNTAXES['default']['source.c++'].parse('function pepe(char *uno) { valor = 1; }', p)
