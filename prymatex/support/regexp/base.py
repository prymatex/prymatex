#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import re
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

def convertRegex(options):
    res = 0x0 | regex.VERSION1
    if 'i' in options:
        res |= regex.IGNORECASE
    if 'm' in options:
        res |= regex.MULTILINE
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

REGEX_COUNTER = 0
RE_COUNTER = 0
ONIG_COUNTER = 0
REGEXPS = []

def compileRegexp(string, flags = []):
    global REGEX_COUNTER, RE_COUNTER, ONIG_COUNTER, REGEXPS
    # 1
    pattern = compileRe(string, flags)
    if pattern is not None:
        RE_COUNTER += 1
        return pattern
    # 2
    pattern = compileRegex(string, flags)
    if pattern is not None:
        REGEX_COUNTER += 1
        return pattern
    # 3
    ONIG_COUNTER += 1
    REGEXPS.append(string)
    return compileOnig(string, flags)
