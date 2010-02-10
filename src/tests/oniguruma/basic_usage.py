#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 10/02/2010 by defo



# tests/py-ctypes/onig
import sys
from os.path import *
pth = abspath('../..') # Hacemos disponible oniguruma
sys.path.append(pth)
from prymatex.lib.ctypes import oniguruma
from  ctypes import *

ONIG_NORMAL = 0

oniguruma.onig_init()
py_pattern = "a(.*)b|[e-f]+"
pattern = c_char_p("a(.*)b|[e-f]+")


string = c_char_p("zzzzaffffffffb")
reg = oniguruma.regex_t()
einfo = oniguruma.OnigErrorInfo()

r = oniguruma.onig_new(pointer(reg), 
                       cast(pattern, POINTER(c_ubyte)), 
                       cast(byref(pattern, len(py_pattern)), POINTER(c_ubyte)),
    0, #oniguruma.ONIG_OPTION_DEFAULT, 
    oniguruma.OnigEncodingASCII, 
    oniguruma.OnigDefaultSyntax, 
    pointer(einfo))
    
if (r != ONIG_NORMAL):
    #char s[ONIG_MAX_ERROR_MESSAGE_LEN];
    s = ''
    oniguruma.onig_error_code_to_str(s, r, byref(einfo))
    print s
    sys.exit()

    
  
#oniguruma

#static UChar* pattern = (UChar* )"a(.*)b|[e-f]+";
#  // Cadena de entrada
#  static UChar* str     = (UChar* )"zzzzaffffffffb";
