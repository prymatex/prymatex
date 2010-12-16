#
# Cython Oniguruma Binding
#

__doc__ = '''
    Oniguruma Binding
'''

from oniguruma_consts import *
from oniguruma_cdefs cimport *


MAX_ERROR_MESSAGE_LEN = 255

class RegexError(Exception):
    pass

class EncodingException(Exception):
    pass

# This structure should be something like
cdef class Match:
    '''
    Matched data
    '''
    #cdef public matches = []
    def __cinit__(self, reg, char *orginal):
        pass
        

    def __len__(self):
        return 0

    def __str__(self):
        return "<Match data at %x" % hash(self)

cdef class Regex:
    '''
    Oniguruma Regex
    '''
    cdef OnigRegex oregexp
    cdef public char* pattern
    cdef public int options
    cdef public name_count
    cdef OnigUChar error_msg[255]

    def __init__(self, char *pattern, int options = OPTION_NONE, 

                 int encoding = ENCODING_ASCII, int syntax = 0):
        '''
        Creates a regular expression instance.
        '''
        raise EncodignException("A")
        self.pattern = strdup(pattern)
        self.options = options
        cdef OnigErrorInfo einfo
        
        cdef int end = <long>self.pattern + strlen( self.pattern )
        
        r = onig_new( &self.oregexp, <OnigUChar *> self.pattern, <OnigUChar *>end, 
                        options, int2encoding( encoding ), 
                        < OnigSyntaxType* > &OnigDefaultSyntax, &einfo)

        if r != NORMAL:
            onig_error_code_to_str(self.error_msg, r, einfo)
            raise Exception(<char *>self.error_msg)
            
        self.name_count = onig_number_of_names(self.oregexp)
        
    def enc_name(self):
        '''
        Returns the enoding name
        '''
        return "%s" % self.oregexp.enc.name
        
    def match(self, char *original):
        '''
        Match. Returns a iterable match
        '''
        m = self._make_match(original)
        return m

    def _make_match(self, char *original):
        ''' Returns the match '''
        cdef OnigRegion *region
        cdef int r
        cdef char *end, *start, *range,
        cdef char *string = strdup(original)
        
        region = onig_region_new()
        
        end = string + len(string)
        start = string
        range = end
        s = string
        
        r = onig_search( self.oregexp, string, end, start, range, region,
                        OPTION_NONE)
        if r >= 0:
            
            if onig_number_of_names(self.oregexp):
                print "There are names"
            else:
                print "No names"
            print "Regions: %d" % region.num_regs
            
            free(string)
            onig_region_free(region, 1 )
            return r
            
        elif r == MISMATCH:
            free(string)
            onig_region_free(region, 1 )
            return None
        else:
            onig_error_code_to_str(self.error_msg, r)
            free(string)
            onig_region_free(region, 1 )
            raise Exception(s)
        
    def __str__(self):
        return "<ORegex %s>" % self.pattern


def set_default_syntax():
    pass
    
def get_default_syntax():
    pass
    
# Module initialization
onig_init()
VERSION = onig_version()
COPYRIGHT = onig_copyright()

# Python's re module compatibility layer

def compile(pattern, flags):
    pass
    
    
    




cdef OnigEncoding int2encoding(int enc):
    '''
    Translates an integer constant into a Encoding
    There must be a less verbose way to acomplish this.
    '''
    if enc == ENCODING_ASCII:
        return &OnigEncodingASCII
    elif enc == ENCODING_ISO_8859_1:
        return &OnigEncodingISO_8859_1
    elif enc == ENCODING_ISO_8859_2:
        return &OnigEncodingISO_8859_2
    elif enc == ENCODING_ISO_8859_3:
        return &OnigEncodingISO_8859_3
    elif enc == ENCODING_ISO_8859_4:
        return &OnigEncodingISO_8859_4
    elif enc == ENCODING_ISO_8859_5:
        return &OnigEncodingISO_8859_5
    elif enc == ENCODING_ISO_8859_6:
        return &OnigEncodingISO_8859_6
    elif enc == ENCODING_ISO_8859_7:
        return &OnigEncodingISO_8859_7
    elif enc == ENCODING_ISO_8859_8:
        return &OnigEncodingISO_8859_8
    elif enc == ENCODING_ISO_8859_9:
        return &OnigEncodingISO_8859_9
    elif enc == ENCODING_ISO_8859_10:
        return &OnigEncodingISO_8859_10
    elif enc == ENCODING_ISO_8859_11:
        return &OnigEncodingISO_8859_11
    elif enc == ENCODING_ISO_8859_13:
        return &OnigEncodingISO_8859_13
    elif enc == ENCODING_ISO_8859_14:
        return &OnigEncodingISO_8859_14
    elif enc == ENCODING_ISO_8859_15:
        return &OnigEncodingISO_8859_15
    elif enc == ENCODING_ISO_8859_16:
        return &OnigEncodingISO_8859_16
    elif enc == ENCODING_UTF8:
        return &OnigEncodingUTF8
    elif enc == ENCODING_UTF16_BE:
        return &OnigEncodingUTF16_BE
    elif enc == ENCODING_UTF16_LE:
        return &OnigEncodingUTF16_LE
    elif enc == ENCODING_UTF32_BE:
        return &OnigEncodingUTF32_BE
    elif enc == ENCODING_UTF32_LE:
        return &OnigEncodingUTF32_LE
    elif enc == ENCODING_EUC_JP:
        return &OnigEncodingEUC_JP
    elif enc == ENCODING_EUC_TW:
        return &OnigEncodingEUC_TW
    elif enc == ENCODING_EUC_KR:
        return &OnigEncodingEUC_KR
    elif enc == ENCODING_EUC_CN:
        return &OnigEncodingEUC_CN
    elif enc == ENCODING_SJIS:
        return &OnigEncodingSJIS
    # Undefined symbol in Ubuntu 10.10 :(
    #elif enc == ENCODING_KOI8_R:
    #    return &OnigEncodingKOI8
    elif enc == ENCODING_CP1251:
        return &OnigEncodingKOI8_R
    elif enc == ENCODING_BIG5:
        return &OnigEncodingBIG5
    elif enc == ENCODING_GB18030:
        return &OnigEncodingGB18030
    raise EncodingException("Encoding number %d not supported" % enc)
 
   
