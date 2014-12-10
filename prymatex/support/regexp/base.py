#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

COMPILERS = []

# =================
#        re
# =================
import re

def convertRe(options):
    res = 0x0
    if 'i' in options:
        res |= re.IGNORECASE
    if 'm' in options:
        res |= re.MULTILINE
    return res

def compileRe(string, flags):
    # Test oniguruma chars
    if any([string.find(tests) != -1 for tests in ["\G", "[[:"]]):
        raise Exception("Pattern")
    return re.compile(string, convertRe(flags))

COMPILERS.append(compileRe)

# =================
#      regex
# =================
try:
    import regex

    # Clases que rompen las pelotas en hexa
    HEXADECIMAL_PATTERNS = [ 
        ("[a-z_\\x{7f}-\\x{ff}]", "[a-zA-Z_]"),
        ("[a-z0-9_\\x{7f}-\\x{ff}]", "[a-zA-Z_]"),
        ("[a-zA-Z_\\x{7f}-\\x{ff}]", "[a-zA-Z_]"),
        ("[a-zA-Z0-9_\\x{7f}-\\x{ff}]", "[a-zA-Z_]"),
        ("[^\\x{00}-\\x{7F}]", "[^a-fA-F0-9_]{2}"),
    ]

    def convertRegex(options):
        res = 0x0 | regex.VERSION1
        if 'i' in options:
            res |= regex.IGNORECASE
        if 'm' in options:
            res |= regex.MULTILINE
        return res

    def compileRegex(string, flags):
        try:
            return regex.compile(string, convertRegex(flags))
        except:
            for od in HEXADECIMAL_PATTERNS:
                string = string.replace(od[0], od[1])
            return regex.compile(string, convertRegex(flags))

    COMPILERS.append(compileRegex)
except:
    logger.warn("In order to run prymatex is highly recommended install regex")

# =================
#   oniguruma
# =================
try:
    import ponyguruma
    from ponyguruma import sre

    def convertOnig(options):
        res = ponyguruma.OPTION_NONE
        if 'i' in options:
            res |= ponyguruma.OPTION_IGNORECASE
        if 's' in options:
            res |= ponyguruma.OPTION_SINGLELINE
        if 'm' in options:
            res |= ponyguruma.OPTION_MULTILINE
        if 'e' in options:
            res |= ponyguruma.OPTION_EXTEND
        return res

    def compileOnig(string, flags):
        return sre.compile(string, convertOnig(flags))

    COMPILERS.append(compileOnig)
except:
    logger.info("Ponyguruma is not installed, don't worry prymatex runs well without it")
    
# =================
#     Compile
# =================
def compileRegexp(string, flags = []):
    for compiler in COMPILERS:
        try:
            return compiler(string, flags)
        except:
            pass
    logger.debug("Ooops, can't compile %s" % string)
