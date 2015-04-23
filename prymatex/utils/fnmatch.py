"""Filename matching with shell patterns.

fnmatch(FILENAME, PATTERN) matches according to the local convention.
fnmatchcase(FILENAME, PATTERN) always takes case in account.

The functions operate by translating the pattern into a regular
expression.  They cache the compiled regular expressions for speed.

The function translate(PATTERN) returns a regular expression
corresponding to PATTERN.  (It does not compile it.)

Based on code from fnmatch.py file distributed with Python 2.6.

Licensed under PSF License (see LICENSE.txt file).

Changes to original fnmatch module:
- translate function supports ``*`` and ``**`` similarly to fnmatch C library
"""

import re

__all__ = ["filter", "fnmatch", "fnmatchcase", "translate"]

_cache = {}
_MAXCACHE = 100

def _purge():
    """Clear the pattern cache"""
    _cache.clear()

def fnmatch(name, pat):
    """Test whether FILENAME matches PATTERN.

    Patterns are Unix shell style:

    - ``*``             matches everything except path separator
    - ``**``            matches everything
    - ``?``             matches any single character
    - ``[seq]``         matches any character in seq
    - ``[!seq]``        matches any char not in seq
    - ``{s1,s2,s3}``    matches any of the strings given (separated by commas)

    An initial period in FILENAME is not special.
    Both FILENAME and PATTERN are first case-normalized
    if the operating system requires it.
    If you don't want this, use fnmatchcase(FILENAME, PATTERN).
    """

    import os
    name = os.path.normcase(name)
    patterns = [ os.path.normcase(pat) ]
    if pat[0] == '{' and pat[-1] == '}':
        patterns = [p for p in pat[1:-1].split(',') if p]
    return any((fnmatchcase(name, pat) for pat in patterns))

def filter(names, pat):
    """Return the subset of the list NAMES that match PAT"""
    import os, posixpath
    result=[]
    pat=os.path.normcase(pat)
    try:
        re_pat = _cache[pat]
    except KeyError:
        res = translate(pat)
        if len(_cache) >= _MAXCACHE:
            _purge()
        _cache[pat] = re_pat = re.compile(res)
    match = re_pat.search
    if os.path is posixpath:
        # normcase on posix is NOP. Optimize it away from the loop.
        for name in names:
            if match(name):
                result.append(name)
    else:
        for name in names:
            if match(os.path.normcase(name)):
                result.append(name)
    return result

def fnmatchcase(name, pat):
    """Test whether FILENAME matches PATTERN, including case.

    This is a version of fnmatch() which doesn't case-normalize
    its arguments.
    """
    
    try:
        re_pat = _cache[pat]
    except KeyError:
        res = translate(pat)
        if len(_cache) >= _MAXCACHE:
            _purge()
        _cache[pat] = re_pat = re.compile(res)
    return re_pat.search(name) is not None

def translate(pat):
    """Translate a shell PATTERN to a regular expression.

    There is no way to quote meta-characters.
    """

    i, n = 0, len(pat)
    res = ''
    while i < n:
        c = pat[i]
        i = i+1
        if c == '*':
            res = res + '.*'
        elif c == '?':
            res = res + '.'
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j+1
            if j < n and pat[j] == ']':
                j = j+1
            while j < n and pat[j] != ']':
                j = j+1
            if j >= n:
                res = res + '\\['
            else:
                stuff = pat[i:j].replace('\\','\\\\')
                i = j+1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                res = '%s[%s]' % (res, stuff)
        else:
            res = res + re.escape(c)
    return res + '\Z(?ms)'

if __name__ == '__main__':
    print(fnmatch("/hola/mundo/pepe.py", "pepe.py"))