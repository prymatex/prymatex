#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

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
            arrays = re.compile("\B-").split(scope)
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
        reg = re.compile( "^%s" % re.escape( pending[-1] ))
        multiplier = self.START_VALUE
        result = 0
        while len(pending) > 0 and current:
            match = reg.search(current)
            if match:
                point_score = (2 ** self.POINT_DEPTH) - current.count( '.' ) + match.group().count( '.' )
                result += point_score * multiplier
                pending.pop()
                if len(pending) > 0:
                    reg = re.compile( "^%s" % re.escape( pending[-1] ) )
            multiplier = multiplier / self.BASE
            reference_array.pop()
            current = reference_array and reference_array[-1] or None
        if len(pending) > 0:
            result = 0
        return result

if __name__ == "__main__":
    sp = PMXScoreManager()
    reference_scope = 'text.html.basic source.php.embedded.html string.quoted.double.php'
      
    print 0, "!=", sp.score( 'source.php string', reference_scope )
    print 0, "!=", sp.score( 'text.html source.php', reference_scope )
    print 0, "==", sp.score( 'string source.php', reference_scope )
    print 0, "==", sp.score( 'source.php text.html', reference_scope )
      
    print 0, "==", sp.score( 'text.html source.php - string', reference_scope )
    print 0, "!=", sp.score( 'text.html source.php - ruby', reference_scope )
      
    print sp.score( '', reference_scope ), " > ", sp.score( 'source.php', reference_scope )
    print sp.score( 'string', reference_scope ), " > ", sp.score( 'source.php', reference_scope ) 
    print sp.score( 'text source string', reference_scope ), " > ", sp.score( 'source string', reference_scope )
      
    print 0, "==", sp.score( 'text.html source.php - string', reference_scope )rce.php - string', reference_scope )
    print 0, "!=", sp.score( 'text.html source.php - 