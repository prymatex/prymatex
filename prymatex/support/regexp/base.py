#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import re, sys
import ponyguruma
from ponyguruma import sre

import regex

ONIG_OPTION_NONE = ponyguruma.OPTION_NONE
ONIG_OPTION_IGNORECASE = ponyguruma.OPTION_IGNORECASE
ONIG_OPTION_SINGLELINE = ponyguruma.OPTION_SINGLELINE
ONIG_OPTION_MULTILINE = ponyguruma.OPTION_MULTILINE
ONIG_OPTION_EXTEND = ponyguruma.OPTION_EXTEND

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

def convertRegex(flags):
    res = 0x0
    return res

def compileRe(string, flags):
    # Test oniguruma chars
    if not any([string.find(tests) != -1 for tests in ["\G", "[[:"]]):
        for o, r in (('?i:', '(?i)'), ):
            string = string.replace(o, r)
        try:
            return re.compile(string, convertRe(flags))
        except:
            pass

def compileRegex(string, flags):
    try:
        return regex.compile(string, convertRegex(flags))
    except:
        pass

def compileOnig(string, flags):
    return sre.compile(string, convertOnig(flags))

def compileRegexp(string, flags = []):
    # 1
    #pattern = compileRegex(string, flags)
    #if pattern is not None:
    #    return pattern
    # 2
    pattern = compileRe(string, flags)
    if pattern is not None:
        return pattern
    # 3
    return compileOnig(string, flags)
