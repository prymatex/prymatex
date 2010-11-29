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
        
    def __len__(self):
        return 0
        
MAX_ERROR_MESSAGE_LEN = 255
    
cdef class Regex:
    '''
    Oniguruma Regex
    '''
    cdef OnigRegex oregexp
    cdef public char* pattern
    cdef public int options
    
    cdef OnigUChar error_msg[255]
    
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
        if r != NORMAL:
            onig_error_code_to_str(self.error_msg, r, einfo)
            raise Exception("Error de compilacion %s" % error_message)
            
        print "El resultado fue %d" % r
        print "Bytes alojados: %d Bytes usados: %d" % ( self.oregexp.alloc, 
                                                        self.oregexp.used)
    
    def match(self, char *string):
        '''
        Match. Should return something iterable
        '''
        cdef OnigRegion *region
        cdef int r
        cdef char *end
        cdef char *start
        cdef char *range
        
        end = string + len(string)
        print "Lenght %d" % len(string)
        start = string
        range = end
        s = string
        print "Let's look for the string %s" % s
        
         
        r = onig_search( self.oregexp, string, end, start, range, region, OPTION_NONE)
        if r >= 0:
            print "Matched %d times :)", r
            return r
            #fprintf(stderr, "match at %d\n\n", r);
            #r = onig_foreach_name(reg, name_callback, (void* )region);
        elif r == MISMATCH:
            return None
        else:
            onig_error_code_to_str(self.error_msg, r)
            raise Exception(s)
            
            
        
    def __str__(self):
        return "<ORegex %s>" % self.pattern[:20]
        


# Module initialization
VERSION = onig_version()
COPYRIGHT = onig_copyright()

