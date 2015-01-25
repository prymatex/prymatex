#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re
import string
import unicodedata
from . import six

# ----------------- White Space tool
RE_WHITESPACE = re.compile(r'([^\S\n]*)', re.UNICODE)
# Match whitespace but not newlines
white_space = lambda text: RE_WHITESPACE.match(text).group(1)

# ----------------- Text convert tools
lower_case = lambda value: value.lower()
upper_case = lambda value: value.upper()
title_case = lambda value: value.title()
transpose = lambda value: value[::-1]
camelcase_to_text = lambda value: re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', ' \\1', value).lower().strip()
text_to_camelcase = lambda value: "".join(value.title().split())

def opposite_case(text):
    newText = ""
    for char in text:
        uindex = string.uppercase.find(char)
        lindex = string.lowercase.find(char)
        if uindex != -1:
            newText += string.lowercase[uindex]
        elif lindex != -1:
            newText += string.uppercase[lindex]
        else:
            newText += char
    return newText

tabs_to_spaces = lambda value, spaceLength = 4: value.replace('\t', ' ' * spaceLength)
spaces_to_tabs = lambda value, spaceLength = 4: value.replace(' ' * spaceLength, '\t')

def asciify(value):
    return unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')

def slugify(value):
    value = asciify(value)
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

def camelify(value):
    value = asciify(value)
    value = re.sub('[^\w\s-]', '', value).strip().title()
    return re.sub('[-\s]+', '', value)

# ----------------- EOL tools --------------------
EOLS = (("\r\n", 'nt', 'DOS/Windows (\\r\\n)'), ("\n", 'posix', 'UNIX (\\n)'), ("\r", 'mac', 'Macintosh (\\r)'))

def get_eol_chars(text):
    """Get text EOL characters"""
    for eol_chars, _os_name, _ in EOLS:
        if text.find(eol_chars) > -1:
            return eol_chars
    return os.linesep

def get_os_name_from_eol_chars(eol_chars):
    """Return OS name from EOL characters"""
    for chars, os_name, _ in EOLS:
        if eol_chars == chars:
            return os_name

def get_eol_chars_from_os_name(os_name):
    """Return EOL characters from OS name"""
    for eol_chars, name, _ in EOLS:
        if name == os_name:
            return eol_chars

def get_eol_chars_from_description(desc):
    """Return EOL characters from OS name"""
    desc = desc.lower()
    for eol_chars, _, description in EOLS:
        if description.lower().find(desc) > -1:
            return eol_chars

def has_mixed_eol_chars(text):
    """Detect if text has mixed EOL characters"""
    eol_chars = get_eol_chars(text)
    if eol_chars is None:
        return False
    correct_text = eol_chars.join((text + eol_chars).splitlines())
    return repr(correct_text) != repr(text)
        
# ------------------ Search
class FuzzyMatcher():
    def __init__(self):
        self.pattern = ''

    def set_pattern(self, pattern):
        self.pattern = '.*?'.join(map(re.escape, list(pattern)))

    def score(self, string):
        match = re.search(self.pattern, string)
        if match is None:
            return 0
        else:
            return 100.0 / ((1 + match.start()) * (match.end() - match.start() + 1))
            
def fuzzy_match(pattern, source):
    if pattern:
        j = 0
        for l in pattern:
            if l == ' ':
                continue
    
            j = source.find(l, j)
            if j == -1:
                return False
    return True