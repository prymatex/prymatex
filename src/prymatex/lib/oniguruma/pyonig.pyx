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


    

cdef class Regex:
    '''
    Oniguruma Regex
    '''
    cdef regex_t *oregexp
    cdef public char* pattern
    cdef public int options

    def __init__(self, char *pattern, int options = OPTION_NONE):
        '''
        Creates a regular expression instance. 
        '''
        
        self.pattern = pattern
        self.options = options
        cdef UChar* pat_ptr = pattern
        cdef OnigErrorInfo einfo 
        
        r = onig_new( &self.oregexp, pattern, self.pattern + len(pattern),
                        options, &OnigEncodingASCII, &OnigSyntaxASIS, &einfo)
        print "El resultado fue %d" % r
        print "Bytes alojados: %d Bytes usados: %d" % ( self.oregexp.alloc, 
                                                        self.oregexp.used)
    
    def match(self, s):
        '''
        Match. Should return something iterable
        '''
        cdef OnigRegion *region
        
        
    def __str__(self):
        return "<ORegex %s>" % self.pattern[:20]
        


# Module initialization
VERSION = onig_version()


