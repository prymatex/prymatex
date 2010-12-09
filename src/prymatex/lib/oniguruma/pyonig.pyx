#
# Cython Oniguruma Binding
#

__doc__ = '''
    Oniguruma Binding
'''

from oniguruma_consts import *
from oniguruma_cdefs cimport *
#from oniguruma_synenc cimport *
#
#
#

cdef extern from "stdlib.h":
    ctypedef unsigned long size_t
    void free(void *ptr)
    void *malloc(size_t size)
    void *realloc(void *ptr, size_t size)
    size_t strlen(char *s)
    char *strcpy(char *dest, char *src)
    char *strdup(char *from_)
    int printf(char *fmt, ...)

from libc cimport stdlib

# This structure should be something like
cdef class Match:
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

    def __init__(self, char *pattern, int options = OPTION_NONE, 
                 encoding = None, syntax = None,):
        '''
        Creates a regular expression instance.
        '''

        self.pattern = strdup(pattern)
        self.options = options
        cdef OnigErrorInfo einfo
        
        cdef int end = <long>self.pattern + strlen( self.pattern )
        
        r = onig_new( &self.oregexp, <OnigUChar *> self.pattern, <OnigUChar *>end, 
                        options, &OnigEncodingASCII, &OnigDefaultSyntax, &einfo)
                        
        if r != NORMAL:
            onig_error_code_to_str(self.error_msg, r, einfo)
            raise Exception("Error de compilacion %s" % error_message)
    
    def enc_name(self):
        '''
        Returns the enoding name
        '''
        return "%s" % self.oregexp.enc.name
        
    def match(self, char *original):
        '''
        Match. Returns a iterable match
        '''
        cdef OnigRegion *region
        cdef int r
        cdef char *end
        cdef char *start
        cdef char *range
        cdef char *string = strdup(original)
        
        region = onig_region_new()
        
        end = string + len(string)
        print "Lenght %d" % len(string)
        start = string
        range = end
        s = string
        
        r = onig_search( self.oregexp, string, end, start, range, region,
                        OPTION_NONE)
        if r >= 0:
            free(string)
            return r
            
        elif r == MISMATCH:
            free(string)
            return None
        else:
            onig_error_code_to_str(self.error_msg, r)
            free(string)
            raise Exception(s)

    def __str__(self):
        return "<ORegex %s>" % self.pattern



# Module initialization
VERSION = onig_version()
COPYRIGHT = onig_copyright()

# Cython definition of oniguruma encodings
cdef OnigEncodingType[30] _onig_encodings
_onig_encodings[:] = [
        OnigEncodingASCII,
        OnigEncodingISO_8859_1,
        OnigEncodingISO_8859_2,
        OnigEncodingISO_8859_3,
        OnigEncodingISO_8859_4,
        OnigEncodingISO_8859_5,
        OnigEncodingISO_8859_6,
        OnigEncodingISO_8859_7,
        OnigEncodingISO_8859_8,
        OnigEncodingISO_8859_9,
        OnigEncodingISO_8859_10,
        OnigEncodingISO_8859_11,
        OnigEncodingISO_8859_13,
        OnigEncodingISO_8859_14,
        OnigEncodingISO_8859_15,
        OnigEncodingISO_8859_16,
        OnigEncodingUTF8,
        OnigEncodingUTF16_BE,
        OnigEncodingUTF16_LE,
        OnigEncodingUTF32_BE,
        OnigEncodingUTF32_LE,
        OnigEncodingEUC_JP,
        OnigEncodingEUC_TW,
        OnigEncodingEUC_KR,
        OnigEncodingEUC_CN,
        OnigEncodingSJIS,
        #OnigEncodingKOI8,
        OnigEncodingKOI8_R,
        OnigEncodingCP1251,
        OnigEncodingBIG5,
        OnigEncodingGB18030,
]
ENCODING_NAMES = []
cdef _get_encoding_names():
    global ENCODING_NAMES 
    for i in range(30):
         name = "%s" % _onig_encodings[i].name
         ENCODING_NAMES.append(name)
          
_get_encoding_names()