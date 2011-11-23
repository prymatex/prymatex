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
        maxi = 0
        for scope in search_scope.split( ',' ):
            arrays =  self.SPLITER.split(scope)
            arrays = map(lambda s: s.strip(), arrays)
            if len(arrays) == 1:
                maxi = max([maxi, self.score_term( arrays[0], reference_scope )])
            elif len(arrays) > 1:
                excluded = False
                for a in arrays[1:]:
                    #Probando forma pedorra de quitar parentesis, a este nivel hay que resolver los parentesis
                    if a[0] == '(' and a[-1] == ')':
                        a = a[1:-1]
                    if self.score_term( a, reference_scope ) > 0:
                        excluded = True
                        break
                if not excluded:
                    maxi = max([maxi, self.score_term( arrays[0], reference_scope )])
            elif len(arrays) < 1:
                raise Exception("Error in scope string: '%s' %s is not a valid number of operands" % (search_scope, len(arrays)))
        return maxi
    
    def score_term(self, search_scope, reference_scope):
        if reference_scope not in self.scores or search_scope not in self.scores[reference_scope]:
            self.scores.setdefault(reference_scope, {})
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
                self.scores[reference_scope][search_scope] = comparation([self.scores[reference_scope][search_scope], self.score_array( scope.split(' '), reference_scope.split(' ') )])
        return self.scores[reference_scope][search_scope]
    
    @classmethod  
    def score_array(cls, search_array, reference_array):
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
        