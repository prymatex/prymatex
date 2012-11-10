#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Source code text utilities
This code was adapted from spyderlib original developed by Pierre Raybaut
spyderlib site:
http://code.google.com/p/spyderlib
"""

import string

to_ascii = lambda s: filter(lambda c: c in string.ascii_letters, s)
to_ascii_cap = lambda s: to_ascii(s).capitalize()

# Order is important:
EOL_CHARS = (("\r\n", 'nt'), ("\n", 'posix'), ("\r", 'mac'))

# ----------------- EOL tools --------------------

def get_eol_chars(text):
    """Get text EOL characters"""
    for eol_chars, _os_name in EOL_CHARS:
        if text.find(eol_chars) > -1:
            return eol_chars


def get_os_name_from_eol_chars(eol_chars):
    """Return OS name from EOL characters"""
    for chars, os_name in EOL_CHARS:
        if eol_chars == chars:
            return os_name


def get_eol_chars_from_os_name(os_name):
    """Return EOL characters from OS name"""
    for eol_chars, name in EOL_CHARS:
        if name == os_name:
            return eol_chars


def has_mixed_eol_chars(text):
    """Detect if text has mixed EOL characters"""
    eol_chars = get_eol_chars(text)
    if eol_chars is None:
        return False
    correct_text = eol_chars.join((text+eol_chars).splitlines())
    return repr(correct_text) != repr(text)


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