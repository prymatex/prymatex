cdef extern from "includes/oniguruma.h":
    #cdef static ONIG_CHAR_TABLE_SIZE = 255
    ctypedef char OnigUChar
    ctypedef OnigUChar UChar
    ctypedef long OnigCodePoint
    ctypedef OnigCodePoint CodePoint
    ctypedef int OnigCtype
    ctypedef int OnigDistance

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
    
    ctypedef struct OnigEncodingType:
          int       mbc_enc_len
          char*     name
          int       max_enc_len
          int       min_enc_len
          int       is_mbc_newline
          OnigCodePoint *mbc_to_code
          int       *code_to_mbclen
          int       *code_to_mbc
          int       *mbc_case_fold
          int       *apply_all_case_fold
          int       *get_case_fold_codes_by_str
          int       *property_name_to_ctype
          int       *is_code_ctype
          int       *get_ctype_code_range
          OnigUChar **left_adjust_char_head
          int       *is_allowed_reverse_match
        
    ctypedef OnigEncodingType* OnigEncoding
    
    
    ctypedef struct OnigCaptureTreeNodeStruct:
        int group
        int beg
        int end
        int allocated
        int num_childs
        OnigCaptureTreeNodeStruct **childs
    
    
    ctypedef OnigCaptureTreeNodeStruct OnigCaptureTreeNode
    
    ctypedef  OnigCaptureTreeNodeStruct* OnigCaptureTreeNode
    
    # /* match result region type */|
    ctypedef struct re_registers:
        int allocated
        int num_regs
        int *beg
        int *end
        OnigCaptureTreeNode *history_root
        
    ctypedef re_registers OnigRegion
    
    ctypedef struct OnigErrorInfo:
        OnigEncoding enc
        OnigUChar* par
        OnigUChar* par_end
       
    ctypedef struct OnigRepeatRange:
        int lower
        int upper
    
    ctypedef unsigned int OnigOptionType
    
    ctypedef struct OnigSyntaxType: 
        unsigned int   op
        unsigned int   op2
        unsigned int   behavior
        OnigOptionType options  #/* default option */
        OnigMetaCharTableType meta_char_table 

        
    ctypedef struct re_pattern_buffer:
          # /* common members of BBuf(bytes-buffer) */
          unsigned char* p          #/* compiled pattern */
          unsigned int used         #/* used space for p */
          unsigned int alloc        #/* allocated space for p */
        
          int state                     #/* normal, searching, compiling */
          int num_mem                   #/* used memory(...) num counted from 1 */
          int num_repeat                #/* OP_REPEAT/OP_REPEAT_NG id-counter */
          int num_null_check            #/* OP_NULL_CHECK_START/END id counter */
          int num_comb_exp_check        #/* combination explosion check */
          int num_call                  #/* number of subexp call */
          unsigned int capture_history  #/* (?@...) flag (1-31) */
          unsigned int bt_mem_start     #/* need backtrack flag */
          unsigned int bt_mem_end       #/* need backtrack flag */
          int stack_pop_level
          int repeat_range_alloc
          OnigRepeatRange* repeat_range
        
          OnigEncoding      enc
          OnigOptionType    options
          OnigSyntaxType*   syntax
          OnigCaseFoldType  case_fold_flag
          void*             name_table
        
          #/* optimization info (string search, char-map and anchors) */
          int            optimize          #/* optimize flag */
          int            threshold_len     #/* search str-length for apply optimize */
          int            anchor            #/* BEGIN_BUF, BEGIN_POS, (SEMI_)END_BUF */
          OnigDistance   anchor_dmin       #/* (SEMI_)END_BUF anchor distance */
          OnigDistance   anchor_dmax       #/* (SEMI_)END_BUF anchor distance */
          int            sub_anchor        #/* start-anchor for exact or map */
          unsigned char *exact
          unsigned char *exact_end
          # Changed
          #unsigned char  char_map[ONIG_CHAR_TABLE_SIZE] #/* used as BM skip or char-map */
          unsigned char  char_map[255] #/* used as BM skip or char-map */
          int           *int_map                   #/* BM skip for exact_len > 255 */
          int           *int_map_backward          #/* BM skip for backward search */
          OnigDistance   dmin                      #/* min-distance of exact or map */
          OnigDistance   dmax                      #/* max-distance of exact or map */
        
          #/* regex_t link chain */
          re_pattern_buffer* chain  #/* escape compile-conflict */
        
    ctypedef re_pattern_buffer OnigRegexType
    ctypedef OnigRegexType* OnigRegex
    
    ctypedef OnigRegexType regex_t
    
    #extern from "includes/oniguruma.h"
    #cdef  class RePatternBuffer(object):
    #    cdef public int x
    #    cdef public int y
        
    ctypedef struct OnigCompileInfo:
        int             num_of_elements
        OnigEncoding    pattern_enc
        OnigEncoding    target_enc
        OnigSyntaxType* syntax
        OnigOptionType  option
        OnigCaseFoldType   case_fold_flag
    
    int onig_init ()
    
    OnigRegion* onig_region_new ()
    
    
    int onig_new (OnigRegex*, OnigUChar* pattern, OnigUChar* pattern_end, 
                    OnigOptionType option, 
                    OnigEncoding enc, 
                    OnigSyntaxType* syntax, 
                    OnigErrorInfo* einfo)
    
    char* onig_version ()
    
    #char[255] onig_error_string
    cdef char onig_error_string[255]
