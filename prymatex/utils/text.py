#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Source code text utilities
This code was adapted from spyderlib original developed by Pierre Raybaut
spyderlib site:
http://code.google.com/p/spyderlib
"""

import re
import string
import difflib

to_ascii = lambda s: filter(lambda c: c in string.ascii_letters, s)
to_ascii_cap = lambda s: to_ascii(s).capitalize()

# Order is important:
EOLS = (("\r\n", 'nt', 'DOS/Windows (\\r\\n)'), ("\n", 'posix', 'UNIX (\\n)'), ("\r", 'mac', 'Macintosh (\\r)'))

# ----------------- EOL tools --------------------
def get_eol_chars(text):
    """Get text EOL characters"""
    for eol_chars, _os_name, _ in EOLS:
        if text.find(eol_chars) > -1:
            return eol_chars


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


def has_mixed_eol_chars(text):
    """Detect if text has mixed EOL characters"""
    eol_chars = get_eol_chars(text)
    if eol_chars is None:
        return False
    correct_text = eol_chars.join((text+eol_chars).splitlines())
    return repr(correct_text) != repr(text)


# ----------------- White Space tool --------------------
RE_WHITESPACE = re.compile(r'^(\s+)', re.UNICODE)
def whiteSpace(text):
    match = RE_WHITESPACE.match(text)
    if match:
        return match.group(0)
    return ''


# ----------------- Python Source tests --------------------
def is_builtin(text):
    """Test if passed string is the name of a Python builtin object"""
    import __builtin__
    return text in [str(name) for name in dir(__builtin__)
                    if not name.startswith('_')]


def is_keyword(text):
    """Test if passed string is the name of a Python keyword"""
    import keyword
    return text in keyword.kwlist


# ----------------- Text convert tools --------------------
lower_case = string.lower
upper_case = string.upper
title_case = lambda text: text.title()
transpose = lambda text: text[::-1]

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

tabs_to_spaces = lambda text, spaceLength = 4: text.replace('\t', ' ' * spaceLength)
spaces_to_tabs = lambda text, spaceLength = 4: text.replace(' ' * spaceLength, '\t')


# ----------------- Text search -------------------------
def subsearch(pattern, text, pstart = 0, tstart = 0, ignoreCase = False):
    if not pattern or not text: []
    if pstart == 0 and ignoreCase:
        pattern = pattern.lower()
        text = text.lower()
    end = len(pattern)
    begin = text.find(pattern, tstart)
    while begin == -1 and end >= 0:
        end -= 1
        begin = text.find(pattern[:end], tstart)
    if end <= 0:
        return []
    return [(pstart, pstart + end, begin, begin + end)] + \
        subsearch(pattern[end:], text, pstart = end, tstart = begin + end)


# ----------------- Text matching -------------------------
def matching_blocks(text1, text2, ratio = 1.0, ignoreCase = False):
    if ignoreCase:
        matcher = difflib.SequenceMatcher(None, text1.lower(), text2.lower())
    else:
        matcher = difflib.SequenceMatcher(None, text1, text2)
    if matcher.ratio() >= ratio:
        print text1, text2, list(matcher.get_grouped_opcodes())
        for matches in matcher.get_grouped_opcodes():
            for match in filter(lambda m: m[0] == 'equal', matches):
                yield match[1:]
                