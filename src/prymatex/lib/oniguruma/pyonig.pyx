cdef extern from "includes/oniguruma.h":

    ctypedef char OnigUChar
    ctypedef long OnigCodePoint
    ctypedef int OnigCtype
    ctypedef int OnigDistnace

    ctypedef struct OnigCaseFoldType:
        int byte_len
        int code_len

    ctypedef struct OnigMetaCharTableType:
        OnigCodePoint esc
        OnigCodePoint anychar
        OnigCodePoint anytime
        OnigCodePoint zero_or_one_time
        OnigCodePoint one_or_more_time
        OnigCodePoint anychar_anytime

    int onigenc_init ()

def init_onig():
    '''
    Initialize
    '''
    onigenc_init()

