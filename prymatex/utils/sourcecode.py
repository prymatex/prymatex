#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import re
import string
import difflib
import unicodedata

to_ascii = lambda s: "".join([c for c in s if c in string.ascii_letters])
to_ascii_cap = lambda s: to_ascii(s).capitalize()

class unaccented_map(dict):
# Translation dictionary.  Translation entries are added to this dictionary as needed.
    CHAR_REPLACEMENT = {
        0xc6: u"AE", # Æ LATIN CAPITAL LETTER AE
        0xd0: u"D",  # Ð LATIN CAPITAL LETTER ETH
        0xd8: u"OE", # Ø LATIN CAPITAL LETTER O WITH STROKE
        0xde: u"Th", # Þ LATIN CAPITAL LETTER THORN
        0xc4: u'Ae', # Ä LATIN CAPITAL LETTER A WITH DIAERESIS
        0xd6: u'Oe', # Ö LATIN CAPITAL LETTER O WITH DIAERESIS
        0xdc: u'Ue', # Ü LATIN CAPITAL LETTER U WITH DIAERESIS
 
        0xc0: u"A", # À LATIN CAPITAL LETTER A WITH GRAVE
        0xc1: u"A", # Á LATIN CAPITAL LETTER A WITH ACUTE
        0xc3: u"A", # Ã LATIN CAPITAL LETTER A WITH TILDE
        0xc7: u"C", # Ç LATIN CAPITAL LETTER C WITH CEDILLA
        0xc8: u"E", # È LATIN CAPITAL LETTER E WITH GRAVE
        0xc9: u"E", # É LATIN CAPITAL LETTER E WITH ACUTE
        0xca: u"E", # Ê LATIN CAPITAL LETTER E WITH CIRCUMFLEX
        0xcc: u"I", # Ì LATIN CAPITAL LETTER I WITH GRAVE
        0xcd: u"I", # Í LATIN CAPITAL LETTER I WITH ACUTE
        0xd2: u"O", # Ò LATIN CAPITAL LETTER O WITH GRAVE
        0xd3: u"O", # Ó LATIN CAPITAL LETTER O WITH ACUTE
        0xd5: u"O", # Õ LATIN CAPITAL LETTER O WITH TILDE
        0xd9: u"U", # Ù LATIN CAPITAL LETTER U WITH GRAVE
        0xda: u"U", # Ú LATIN CAPITAL LETTER U WITH ACUTE
 
        0xdf: u"ss", # ß LATIN SMALL LETTER SHARP S
        0xe6: u"ae", # æ LATIN SMALL LETTER AE
        0xf0: u"d",  # ð LATIN SMALL LETTER ETH
        0xf8: u"oe", # ø LATIN SMALL LETTER O WITH STROKE
        0xfe: u"th", # þ LATIN SMALL LETTER THORN,
        0xe4: u'ae', # ä LATIN SMALL LETTER A WITH DIAERESIS
        0xf6: u'oe', # ö LATIN SMALL LETTER O WITH DIAERESIS
        0xfc: u'ue', # ü LATIN SMALL LETTER U WITH DIAERESIS
 
        0xe0: u"a", # à LATIN SMALL LETTER A WITH GRAVE
        0xe1: u"a", # á LATIN SMALL LETTER A WITH ACUTE
        0xe3: u"a", # ã LATIN SMALL LETTER A WITH TILDE
        0xe7: u"c", # ç LATIN SMALL LETTER C WITH CEDILLA
        0xe8: u"e", # è LATIN SMALL LETTER E WITH GRAVE
        0xe9: u"e", # é LATIN SMALL LETTER E WITH ACUTE
        0xea: u"e", # ê LATIN SMALL LETTER E WITH CIRCUMFLEX
        0xec: u"i", # ì LATIN SMALL LETTER I WITH GRAVE
        0xed: u"i", # í LATIN SMALL LETTER I WITH ACUTE
        0xf2: u"o", # ò LATIN SMALL LETTER O WITH GRAVE
        0xf3: u"o", # ó LATIN SMALL LETTER O WITH ACUTE
        0xf5: u"o", # õ LATIN SMALL LETTER O WITH TILDE
        0xf9: u"u", # ù LATIN SMALL LETTER U WITH GRAVE
        0xfa: u"u", # ú LATIN SMALL LETTER U WITH ACUTE
 
        0x2018: u"'", # ‘ LEFT SINGLE QUOTATION MARK
        0x2019: u"'", # ’ RIGHT SINGLE QUOTATION MARK
        0x201c: u'"', # “ LEFT DOUBLE QUOTATION MARK
        0x201d: u'"', # ” RIGHT DOUBLE QUOTATION MARK
 
        }
 
    # Maps a unicode character code (the key) to a replacement code
    # (either a character code or a unicode string).
    def mapchar(self, key):
        ch = self.get(key)
        if ch is not None:
            return ch
        try:
            de = unicodedata.decomposition(unichr(key))
            p1, p2 = [int(x, 16) for x in de.split(None, 1)]
            if p2 == 0x308:
		ch = self.CHAR_REPLACEMENT.get(key)
            else:
                ch = int(p1)
 
        except (IndexError, ValueError):
            ch = self.CHAR_REPLACEMENT.get(key, key)
        self[key] = ch
        return ch
 
    if sys.version >= "2.5":
        # use __missing__ where available
        __missing__ = mapchar
    else:
        # otherwise, use standard __getitem__ hook (this is slower,
        # since it's called for each character)
        __getitem__ = mapchar
 
char_mapper = unaccented_map()

# ----------------- EOL tools --------------------
EOLS = (("\r\n", 'nt', 'DOS/Windows (\\r\\n)'), ("\n", 'posix', 'UNIX (\\n)'), ("\r", 'mac', 'Macintosh (\\r)'))

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
    correct_text = eol_chars.join((text + eol_chars).splitlines())
    return repr(correct_text) != repr(text)

# ----------------- White Space tool --------------------
# Match whitespace but not newlines
RE_WHITESPACE = re.compile(r'([^\S\n]*)', re.UNICODE)
def whiteSpace(text):
    return RE_WHITESPACE.match(text).group(1)

# ----------------- Python Source tests --------------------
def is_builtin(text):
    """Test if passed string is the name of a Python builtin object"""
    import builtins
    return text in [str(name) for name in dir(__builtin__)
                    if not name.startswith('_')]

def is_keyword(text):
    """Test if passed string is the name of a Python keyword"""
    import keyword
    return text in keyword.kwlist

# ----------------- Text convert tools --------------------
lower_case = lambda text: text.lower()
upper_case = lambda text: text.upper()
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

def asciify(text):
    try:
        return text.encode('ascii')
    except AttributeError:
        return str(text).encode('ascii')
    except UnicodeEncodeError:
        return unicodedata.normalize('NFKD', text.translate(char_mapper)).encode('ascii', 'replace')

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
        print(text1, text2, list(matcher.get_grouped_opcodes()))
        for matches in matcher.get_grouped_opcodes():
            for match in [m for m in matches if m[0] == 'equal']:
                yield match[1:]
