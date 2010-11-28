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

# This structure should be something like
cdef class OregexMatch:
    '''
    Matched data
    '''
    def __cinit__(self):
        pass
    
cdef class Regex:
    '''
    Oniguruma Regex
    '''
    cdef regex_t *oregexp
    cdef public char* pattern
    cdef public int options
    #cdef char error_message[MAX_ERROR_MESSAGE_LEN] 
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
        #if r != NORMAL:
        #    onig_error_code_to_str(error_message, r, einfo)
        #    raise Exception("Error de compilacion %s" % error_message)
            
        print "El resultado fue %d" % r
        print "Bytes alojados: %d Bytes usados: %d" % ( self.oregexp.alloc, 
                                                        self.oregexp.used)
    
    def match(self, s):
        '''
        Match. Should return something iterable
        '''
        cdef OnigRegion *region
        return OregexMatch()
        
        
    def __str__(self):
        return "<ORegex %s>" % self.pattern[:20]
        


# Module initialization
VERSION = onig_version()


