#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import string
import unicodedata
from . import six

# ---------- Translation dictionary.
# Translation entries are added to this dictionary as needed.
class unaccented_map(dict):
    CHAR_REPLACEMENT = {
        0xc6: "AE", # Æ LATIN CAPITAL LETTER AE
        0xd0: "D",  # Ð LATIN CAPITAL LETTER ETH
        0xd8: "OE", # Ø LATIN CAPITAL LETTER O WITH STROKE
        0xde: "Th", # Þ LATIN CAPITAL LETTER THORN
        0xc4: 'Ae', # Ä LATIN CAPITAL LETTER A WITH DIAERESIS
        0xd6: 'Oe', # Ö LATIN CAPITAL LETTER O WITH DIAERESIS
        0xdc: 'Ue', # Ü LATIN CAPITAL LETTER U WITH DIAERESIS
 
        0xc0: "A", # À LATIN CAPITAL LETTER A WITH GRAVE
        0xc1: "A", # Á LATIN CAPITAL LETTER A WITH ACUTE
        0xc3: "A", # Ã LATIN CAPITAL LETTER A WITH TILDE
        0xc7: "C", # Ç LATIN CAPITAL LETTER C WITH CEDILLA
        0xc8: "E", # È LATIN CAPITAL LETTER E WITH GRAVE
        0xc9: "E", # É LATIN CAPITAL LETTER E WITH ACUTE
        0xca: "E", # Ê LATIN CAPITAL LETTER E WITH CIRCUMFLEX
        0xcc: "I", # Ì LATIN CAPITAL LETTER I WITH GRAVE
        0xcd: "I", # Í LATIN CAPITAL LETTER I WITH ACUTE
        0xd2: "O", # Ò LATIN CAPITAL LETTER O WITH GRAVE
        0xd3: "O", # Ó LATIN CAPITAL LETTER O WITH ACUTE
        0xd5: "O", # Õ LATIN CAPITAL LETTER O WITH TILDE
        0xd9: "U", # Ù LATIN CAPITAL LETTER U WITH GRAVE
        0xda: "U", # Ú LATIN CAPITAL LETTER U WITH ACUTE
 
        0xdf: "ss", # ß LATIN SMALL LETTER SHARP S
        0xe6: "ae", # æ LATIN SMALL LETTER AE
        0xf0: "d",  # ð LATIN SMALL LETTER ETH
        0xf8: "oe", # ø LATIN SMALL LETTER O WITH STROKE
        0xfe: "th", # þ LATIN SMALL LETTER THORN,
        0xe4: 'ae', # ä LATIN SMALL LETTER A WITH DIAERESIS
        0xf6: 'oe', # ö LATIN SMALL LETTER O WITH DIAERESIS
        0xfc: 'ue', # ü LATIN SMALL LETTER U WITH DIAERESIS
 
        0xe0: "a", # à LATIN SMALL LETTER A WITH GRAVE
        0xe1: "a", # á LATIN SMALL LETTER A WITH ACUTE
        0xe3: "a", # ã LATIN SMALL LETTER A WITH TILDE
        0xe7: "c", # ç LATIN SMALL LETTER C WITH CEDILLA
        0xe8: "e", # è LATIN SMALL LETTER E WITH GRAVE
        0xe9: "e", # é LATIN SMALL LETTER E WITH ACUTE
        0xea: "e", # ê LATIN SMALL LETTER E WITH CIRCUMFLEX
        0xec: "i", # ì LATIN SMALL LETTER I WITH GRAVE
        0xed: "i", # í LATIN SMALL LETTER I WITH ACUTE
        0xf2: "o", # ò LATIN SMALL LETTER O WITH GRAVE
        0xf3: "o", # ó LATIN SMALL LETTER O WITH ACUTE
        0xf5: "o", # õ LATIN SMALL LETTER O WITH TILDE
        0xf9: "u", # ù LATIN SMALL LETTER U WITH GRAVE
        0xfa: "u", # ú LATIN SMALL LETTER U WITH ACUTE
 
        0x2018: "'", # ‘ LEFT SINGLE QUOTATION MARK
        0x2019: "'", # ’ RIGHT SINGLE QUOTATION MARK
        0x201c: '"', # “ LEFT DOUBLE QUOTATION MARK
        0x201d: '"', # ” RIGHT DOUBLE QUOTATION MARK
 
        }
 
    # Maps a unicode character code (the key) to a replacement code
    # (either a character code or a unicode string).
    def __missing__(self, key):
        ch = self.get(key)
        if ch is not None:
            return ch
        try:
            de = unicodedata.decomposition(six.PY3 and chr(key) or unichr(key))
            p1, p2 = [int(x, 16) for x in de.split(None, 1)]
            if p2 == 0x308:
                ch = self.CHAR_REPLACEMENT.get(key)
            else:
                ch = int(p1)
 
        except (IndexError, ValueError):
            ch = self.CHAR_REPLACEMENT.get(key, key)
        self[key] = ch
        return ch
 
char_mapper = unaccented_map()

# ----------------- White Space tool
RE_WHITESPACE = re.compile(r'([^\S\n]*)', re.UNICODE)
# Match whitespace but not newlines
white_space = lambda text: RE_WHITESPACE.match(text).group(1)

# ----------------- Text convert tools
def _remove_characters(source, characters):
    for char in source:
        if char in characters:
            yield char

to_ascii = lambda source: "".join(_remove_characters(source, string.ascii_letters))
to_alphanumeric = lambda source: "".join(_remove_characters(source, string.ascii_letters + string.digits))
lower_case = lambda text: text.lower()
upper_case = lambda text: text.upper()
title_case = lambda text: text.title()
transpose = lambda text: text[::-1]
camelcase_to_text = lambda camelcase: re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', ' \\1', camelcase).lower().strip()
text_to_camelcase = lambda text: "".join(text.title().split())

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
        return text.encode('ascii').decode()
    except UnicodeEncodeError:
        return unicodedata.normalize('NFKD', text.translate(char_mapper))

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