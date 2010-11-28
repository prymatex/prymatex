cdef extern from "includes/oniguruma.h":

    #
    # Type definitions
    #
    
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
    
    ctypedef OnigSyntaxType* OnigSyntax
        
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
    
    # Error string
    cdef char onig_error_string[255]
    
    #
    # Syntaxes
    #
    
    OnigSyntaxType OnigSyntaxASIS
    OnigSyntaxType OnigSyntaxPosixBasic
    OnigSyntaxType OnigSyntaxPosixExtended
    OnigSyntaxType OnigSyntaxEmacs
    OnigSyntaxType OnigSyntaxGrep
    OnigSyntaxType OnigSyntaxGnuRegex
    OnigSyntaxType OnigSyntaxJava
    OnigSyntaxType OnigSyntaxPerl
    OnigSyntaxType OnigSyntaxPerl_NG
    OnigSyntaxType OnigSyntaxRuby
    
    #
    # Encodings
    #
    
    OnigEncodingType OnigEncodingASCII
    OnigEncodingType OnigEncodingISO_8859_1
    OnigEncodingType OnigEncodingISO_8859_2
    OnigEncodingType OnigEncodingISO_8859_3
    OnigEncodingType OnigEncodingISO_8859_4
    OnigEncodingType OnigEncodingISO_8859_5
    OnigEncodingType OnigEncodingISO_8859_6
    OnigEncodingType OnigEncodingISO_8859_7
    OnigEncodingType OnigEncodingISO_8859_8
    OnigEncodingType OnigEncodingISO_8859_9
    OnigEncodingType OnigEncodingISO_8859_10
    OnigEncodingType OnigEncodingISO_8859_11
    OnigEncodingType OnigEncodingISO_8859_13
    OnigEncodingType OnigEncodingISO_8859_14
    OnigEncodingType OnigEncodingISO_8859_15
    OnigEncodingType OnigEncodingISO_8859_16
    OnigEncodingType OnigEncodingUTF8
    OnigEncodingType OnigEncodingUTF16_BE
    OnigEncodingType OnigEncodingUTF16_LE
    OnigEncodingType OnigEncodingUTF32_BE
    OnigEncodingType OnigEncodingUTF32_LE
    OnigEncodingType OnigEncodingEUC_JP
    OnigEncodingType OnigEncodingEUC_TW
    OnigEncodingType OnigEncodingEUC_KR
    OnigEncodingType OnigEncodingEUC_CN
    OnigEncodingType OnigEncodingSJIS
    OnigEncodingType OnigEncodingKOI8
    OnigEncodingType OnigEncodingKOI8_R
    OnigEncodingType OnigEncodingCP1251
    OnigEncodingType OnigEncodingBIG5
    OnigEncodingType OnigEncodingGB18030
    
    #
    # Function signatures
    #
    
    # Oniguruma Native API
    int onig_init ()
    int onig_error_code_to_str (OnigUChar* s, int err_code, ...)
    #void onig_set_warn_func (OnigWarnFunc f)
    #void onig_set_verb_warn_func (OnigWarnFunc f)
    int onig_new (OnigRegex*,  OnigUChar* pattern,  OnigUChar* pattern_end, OnigOptionType option, OnigEncoding enc, OnigSyntaxType* syntax, OnigErrorInfo* einfo)
    int onig_new_deluxe (OnigRegex* reg,  OnigUChar* pattern,  OnigUChar* pattern_end, OnigCompileInfo* ci, OnigErrorInfo* einfo)
    void onig_free (OnigRegex)
    int onig_recompile (OnigRegex,  OnigUChar* pattern,  OnigUChar* pattern_end, OnigOptionType option, OnigEncoding enc, OnigSyntaxType* syntax, OnigErrorInfo* einfo)
    int onig_recompile_deluxe (OnigRegex reg,  OnigUChar* pattern,  OnigUChar* pattern_end, OnigCompileInfo* ci, OnigErrorInfo* einfo)
    int onig_search (OnigRegex,  OnigUChar* str,  OnigUChar* end,  OnigUChar* start,  OnigUChar* range, OnigRegion* region, OnigOptionType option)
    int onig_match (OnigRegex,  OnigUChar* str,  OnigUChar* end,  OnigUChar* at, OnigRegion* region, OnigOptionType option)
    OnigRegion* onig_region_new ()
    void onig_region_init (OnigRegion* region)
    void onig_region_free (OnigRegion* region, int free_self)
    void onig_region_copy (OnigRegion* to, OnigRegion* from_)
    void onig_region_clear (OnigRegion* region)
    int onig_region_resize (OnigRegion* region, int n)
    int onig_region_set (OnigRegion* region, int at, int beg, int end)
    int onig_name_to_group_numbers (OnigRegex reg,  OnigUChar* name,  OnigUChar* name_end, int** nums)
    int onig_name_to_backref_number (OnigRegex reg,  OnigUChar* name,  OnigUChar* name_end, OnigRegion *region)
    int onig_foreach_name (OnigRegex reg, int (*func)( OnigUChar*,  OnigUChar*,int,int*,OnigRegex,void*), void* arg)
    int onig_number_of_names (OnigRegex reg)
    int onig_number_of_captures (OnigRegex reg)
    int onig_number_of_capture_histories (OnigRegex reg)
    OnigCaptureTreeNode* onig_get_capture_tree (OnigRegion* region)
    int onig_capture_tree_traverse (OnigRegion* region, int at, int(*callback_func)(int,int,int,int,int,void*), void* arg)
    int onig_noname_group_capture_is_active (OnigRegex reg)
    OnigEncoding onig_get_encoding (OnigRegex reg)
    OnigOptionType onig_get_options (OnigRegex reg)
    OnigCaseFoldType onig_get_case_fold_flag (OnigRegex reg)
    OnigSyntaxType* onig_get_syntax (OnigRegex reg)
    int onig_set_default_syntax (OnigSyntaxType* syntax)
    void onig_copy_syntax (OnigSyntaxType* to, OnigSyntaxType* from_)
    unsigned int onig_get_syntax_op (OnigSyntaxType* syntax)
    unsigned int onig_get_syntax_op2 (OnigSyntaxType* syntax)
    unsigned int onig_get_syntax_behavior (OnigSyntaxType* syntax)
    OnigOptionType onig_get_syntax_options (OnigSyntaxType* syntax)
    void onig_set_syntax_op (OnigSyntaxType* syntax, unsigned int op)
    void onig_set_syntax_op2 (OnigSyntaxType* syntax, unsigned int op2)
    void onig_set_syntax_behavior (OnigSyntaxType* syntax, unsigned int behavior)
    void onig_set_syntax_options (OnigSyntaxType* syntax, OnigOptionType options)
    int onig_set_meta_char (OnigSyntaxType* syntax, unsigned int what, OnigCodePoint code)
    void onig_copy_encoding (OnigEncoding to, OnigEncoding from_)
    OnigCaseFoldType onig_get_default_case_fold_flag ()
    int onig_set_default_case_fold_flag (OnigCaseFoldType case_fold_flag)
    unsigned int onig_get_match_stack_limit_size ()
    int onig_set_match_stack_limit_size (unsigned int size)
    int onig_end ()
    char* onig_version ()
    char* onig_copyright ()

        