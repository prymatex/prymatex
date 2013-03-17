#!/usr/bin/env python
# encoding: utf-8

import re, ponyguruma
from ponyguruma import sre
ONIG_OPTION_NONE = ponyguruma.OPTION_NONE
ONIG_OPTION_IGNORECASE = ponyguruma.OPTION_IGNORECASE
ONIG_OPTION_SINGLELINE = ponyguruma.OPTION_SINGLELINE
ONIG_OPTION_MULTILINE = ponyguruma.OPTION_MULTILINE
ONIG_OPTION_EXTEND = ponyguruma.OPTION_EXTEND

RE_OPTION_MULTILINE = re.MULTILINE

RE_REPLACES = (
    ('?i:', '(?i)')
)

def convertOnig(options):
    res = ONIG_OPTION_NONE
    if 'i' in options:
        res |= ONIG_OPTION_IGNORECASE
    if 's' in options:
        res |= ONIG_OPTION_SINGLELINE
    if 'm' in options:
        res |= ONIG_OPTION_MULTILINE
    if 'e' in options:
        res |= ONIG_OPTION_EXTEND
    return res

def convertRe(options):
    res = 0x0
    if 'i' in options:
        res |= re.IGNORECASE
    if 'm' in options:
        res |= re.MULTILINE
    return res

def compileRe(string, flags):
    # Test oniguruma chars
    if not any(map(lambda tests : string.find(tests) != -1, ["\G"])):
        for repl in RE_REPLACES:
            string = string.replace(repl[0], repl[1])
        try:
            return re.compile(string, convertRe(flags))
        except:
            pass

def compileOnig(string, flags):
    return sre.compile(string, convertOnig(flags))

def compileRegexp(string, flags = []):
    string = unicode(string)
    pattern = compileRe(string, flags)
    if pattern is None:
        pattern = compileOnig(string, flags)
    return pattern
