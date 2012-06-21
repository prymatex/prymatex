#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

#=============================================== 
# ScoreManager
#=============================================== 

class PMXScoreManager(object):
    POINT_DEPTH    = 4
    NESTING_DEPTH  = 40
    START_VALUE    = 2 ** ( POINT_DEPTH * NESTING_DEPTH )
    BASE           = 2 ** POINT_DEPTH
    SPLITER        = re.compile("\B-")
    OR             = " | "
    AND            = " & "
    def __init__(self):
        self.scores = {}
    
    def score(self, search_scope, reference_scope):
        if reference_scope not in self.scores or search_scope not in self.scores[reference_scope]:
            #Guardo resultados finales
            self.scores.setdefault(reference_scope, {})
            maxi = 0
            for scope in search_scope.split( ',' ):
                arrays =  self.SPLITER.split(scope)
                arrays = map(lambda s: s.strip(), arrays)
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
            self.scores[reference_scope][search_scope] = maxi
        return self.scores[reference_scope][search_scope]

    def score_term(self, search_scope, reference_scope):
        if reference_scope not in self.scores or search_scope not in self.scores[reference_scope]:
            #Guardo resultados parciales
            self.scores.setdefault(reference_scope, {})
            #Parentesis
            if search_scope.startswith("(") and search_scope.endswith(")"):
                search_scope = search_scope[1:-1]
            if search_scope.find(self.OR):
                comparation = max
                scopes = search_scope.split(self.OR)
            elif search_scope.find(self.AND):
                comparation = min
                scopes = search_scope.split(self.AND)
            else:
                comparation = max
                scopes = [ search_scope ]
            self.scores[reference_scope][search_scope] = 0
            for scope in scopes:
                self.scores[reference_scope][search_scope] = comparation([self.scores[reference_scope][search_scope], self.score_array_startswith( scope.split(' '), reference_scope.split(' ') )])
        return self.scores[reference_scope][search_scope]
    
    @classmethod  
    def score_array_regexp(cls, search_array, reference_array):
        pending = search_array
        current = reference_array[-1]
        reg = re.compile( "^%s" % re.escape( pending[-1] ))
        multiplier = cls.START_VALUE
        result = 0
        while len(pending) > 0 and current:
            match = reg.search(current)
            if match:
                point_score = (2 ** cls.POINT_DEPTH) - current.count( '.' ) + match.group().count( '.' )
                result += point_score * multiplier
                pending.pop()
                if len(pending) > 0:
                    reg = re.compile( "^%s" % re.escape( pending[-1] ) )
            multiplier = multiplier / cls.BASE
            reference_array.pop()
            current = reference_array[-1] if reference_array else None
        if len(pending) > 0:
            result = 0
        return result
        
    @classmethod  
    def score_array_startswith(cls, search_array, reference_array):
        """ Esta funcion pretende apurar el trabajo de obtener el score trabajando con cadenas en lugar de usar regexp """
        pending = search_array
        currentReference = reference_array[-1]
        currentPending = pending[-1]
        multiplier = cls.START_VALUE
        result = 0
        while pending and currentReference and currentPending:
            if currentReference == currentPending or currentReference.startswith("%s." % currentPending):
                point_score = (2 ** cls.POINT_DEPTH) - currentReference.count( '.' ) + currentPending.count( '.' )
                result += point_score * multiplier
                pending.pop()
                currentPending = pending[-1] if pending else None
            multiplier = multiplier / cls.BASE
            reference_array.pop()
            currentReference = reference_array[-1] if reference_array else None
        if pending:
            return 0
        return result
        
    # TODO DebugME
    @classmethod  
    def score_array_startswith_index(cls, search_array, reference_array):
        """ Esta funcion pretende apurar el trabajo de obtener el score no usando los pop's y trabajando con cadenas """
        lenSearch = -len(search_array)
        lenReference = -len(reference_array)
        indexReference = indexPending = -1
        multiplier = cls.START_VALUE
        result = 0
        while indexPending >= lenSearch and indexReference >= lenReference:
            if reference_array[indexReference] == search_array[indexPending] or reference_array[indexReference].startswith("%s." % search_array[indexPending]):
                point_score = (2 ** cls.POINT_DEPTH) - reference_array[indexReference].count( '.' ) + search_array[indexPending].count( '.' )
                result += point_score * multiplier
                indexPending -= 1
            multiplier = multiplier / cls.BASE
            indexReference -= 1
        if indexPending > lenSearch:
            return 0
        return result
        
if __name__ == '__main__':
    scoreManager = PMXScoreManager()
    scope = "text.html -(meta.tag | source), invalid.illegal.incomplete.html -source"
    reference = "text.html meta.tag source"
    print scoreManager.score(scope, reference)
    scope = "text.html meta.tag -(entity.other.attribute-name | punctuation.definition.tag.begin | source | entity.name.tag | string | invalid.illegal.incomplete.html)"
    print scoreManager.score(scope, reference)
    print scoreManager.scores
    reference = "source.python string.quoted.double.single-line.python punctuation.definition.string.end.python meta.empty-string.double.python"
    for _ in xrange(10000):
        scoreManager = PMXScoreManager()
        scope = "source.python string.quoted.double.single-line punctuation.definition.string.end.python"
        scoreManager.score(scope, reference)
    