#
# Cython Oniguruma Binding
#

__doc__ = '''
    Oniguruma Binding
'''

from oniguruma_consts import *
from oniguruma_cdefs cimport *

#
#
#

from libc cimport stdlib

class Regex:
    '''
    Oniguruma Regex
    '''
    def __init__(self, char *pattern, int options = ONIG_OPTION_NONE):
        cdef regex_t *c_oregexp 
        self.pattern = pattern
        self.options = options
        cdef UChar* pat_ptr = pattern
    
    def match(self, s):
        '''
        Match. Should return something iterable
        '''
        pass 
        
    def __str__(self):
        return "<ORegex %s>" % self.pattern[:20]
        


# Module initialization
VERSION = onig_version()

