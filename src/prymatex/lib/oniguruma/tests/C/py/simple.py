'''
Created on 14/11/2010

@author: defo

'''

import sys
from os.path import join, abspath, dirname
ONIG_PATH = abspath(join(dirname(__file__), '..', '..', '..', '..'))
#print ONIG_PATH
sys.path.append(ONIG_PATH)

from oniguruma import OnigErrorInfo, OnigRegion, OnigUChar, OnigEncodingASCII
from oniguruma import OnigDefaultSyntax
from oniguruma import regex_t, onig_new, onig_region_new, onig_search 
from ctypes import POINTER, create_string_buffer, pointer, byref, c_char_p,\
    c_ubyte
from ctypes import addressof, cast
#/*
# * simple.c
# */
##include <stdio.h>
##include <string.h>
##include "oniguruma.h"
#
#extern int main(int argc, char* argv[])
#{
#  int r;
#  unsigned char *start, *range, *end;
start = POINTER(c_ubyte)()
end = POINTER(c_ubyte)()
range = POINTER(c_ubyte)()
#  regex_t* reg;
reg = regex_t()
#  OnigErrorInfo einfo;
einfo = OnigErrorInfo()
#  OnigRegion *region;
region = OnigRegion()

#UCharP = POINTER(OnigUChar)


#  static UChar* pattern = (UChar* )"a(.*)b|[e-f]+";
pattern = create_string_buffer("a(.*)b|[e-f]+")
print "Buffer", pattern

#  static UChar* str     = (UChar* )"zzzzaffffffffb";
str = create_string_buffer("zzzzaffffffffb")


#  r = onig_new(&reg, pattern, pattern + strlen((char* )pattern),
#    ONIG_OPTION_DEFAULT, ONIG_ENCODING_ASCII, ONIG_SYNTAX_DEFAULT, &einfo);


r = onig_new(cast(byref(reg), POINTER(regex_t)), 
             cast(byref(pattern), POINTER(OnigUChar)), 
             cast(byref(pattern, len(pattern.value)), POINTER(OnigUChar)),
             0, 
             OnigEncodingASCII, 
             OnigDefaultSyntax, 
             cast(byref(einfo), POINTER(OnigErrorInfo)))
## 
if r != 0:
    print "Error"
#  if (r != ONIG_NORMAL) {
#    char s[ONIG_MAX_ERROR_MESSAGE_LEN];
#    onig_error_code_to_str(s, r, &einfo);
#    fprintf(stderr, "ERROR: %s\n", s);
#    return -1;
#  }
#
#  region = onig_region_new();
region = onig_region_new()
#
#  end   = str + strlen((char* )str);
print "L", len(str.value)
end = cast(byref(str, len(str.value)), POINTER(OnigUChar))
print addressof(str)
#  start = str;
start = cast(byref(str), POINTER(OnigUChar))
#  range = end;
range = cast(byref(str, len(str.value)), POINTER(OnigUChar))
print range
from ipdb import set_trace; set_trace()
#  r = onig_search(reg, str, end, start, range, region, ONIG_OPTION_NONE);
r = onig_search(reg, 
                cast(byref(str), POINTER(OnigUChar)), 
                end, 
                start, 
                range, 
                region, 
                0 #ONIG_OPTION_NONE
                )
print r

#  if (r >= 0) {
#    int i;
#
#    fprintf(stderr, "match at %d\n", r);
#    for (i = 0; i < region->num_regs; i++) {
#      fprintf(stderr, "%d: (%d-%d)\n", i, region->beg[i], region->end[i]);
#    }
#  }
#  else if (r == ONIG_MISMATCH) {
#    fprintf(stderr, "search fail\n");
#  }
#  else { /* error */
#    char s[ONIG_MAX_ERROR_MESSAGE_LEN];
#    onig_error_code_to_str(s, r);
#    fprintf(stderr, "ERROR: %s\n", s);
#    return -1;
#  }
#
#  onig_region_free(region, 1 /* 1:free self, 0:free contents only */);
#  onig_free(reg);
#  onig_end();
#  return 0;
#}


