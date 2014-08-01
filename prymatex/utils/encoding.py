#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""Source code text utilities
This code was adapted from spyderlib original developed by Pierre Raybaut
spyderlib site:
http://code.google.com/p/spyderlib
"""

import re, os, locale, sys
from codecs import BOM_UTF8, BOM_UTF16, BOM_UTF32

from . import six

PREFERRED_ENCODING = locale.getpreferredencoding()

# The default encoding for file paths and environment variables should be set
# to match the default encoding that the OS is using.
def getfilesystemencoding():
    """
    Query the filesystem for the encoding used to encode filenames
    and environment variables.
    """
    encoding = sys.getfilesystemencoding()
    if encoding is None:
        # Must be Linux or Unix and nl_langinfo(CODESET) failed.
        encoding = PREFERRED_ENCODING
    return encoding

FS_ENCODING = getfilesystemencoding()

def transcode(text, input = PREFERRED_ENCODING, output = PREFERRED_ENCODING):
    """Transcode a text string"""
    try:
        return text.decode("cp437").encode("cp1252")
    except UnicodeError:
        try:
            return text.decode("cp437").encode(output)
        except UnicodeError:
            return text

#------------------------------------------------------------------------------
#  Functions for encoding and decoding *text data* itself, usually originating
#  from or destined for the *contents* of a file.
#------------------------------------------------------------------------------

# Codecs for working with files and text.
CODING_RE = re.compile("coding[:=]\s*([-\w_.]+)")
CODECS = []
with open(os.path.join(os.path.dirname(__file__), "codecs")) as openFile:
    for line in openFile.read().splitlines():
        CODECS.append(tuple(line.split(";")))

def get_coding(text):
    """
    Function to get the coding of a text.
    @param text text to inspect (string)
    @return coding string
    """
    for line in text.splitlines()[:2]:
        result = CODING_RE.search(six.text_type(line))
        if result:
            return result.group(1)
    return None

def decode(text):
    """
    Function to decode a text.
    @param text text to decode (string)
    @return decoded text and encoding
    """
    try:
        if text.startswith(BOM_UTF8):
            # UTF-8 with BOM
            return six.text_type(text[len(BOM_UTF8):], 'utf-8'), 'utf-8-bom'
        elif text.startswith(BOM_UTF16):
            # UTF-16 with BOM
            return six.text_type(text[len(BOM_UTF16):], 'utf-16'), 'utf-16'
        elif text.startswith(BOM_UTF32):
            # UTF-32 with BOM
            return six.text_type(text[len(BOM_UTF32):], 'utf-32'), 'utf-32'
        coding = get_coding(text)
        if coding:
            return six.text_type(text, coding), coding
    except (UnicodeError, LookupError):
        pass
    # Assume UTF-8
    try:
        return six.text_type(text, 'utf-8'), 'utf-8-guessed'
    except (UnicodeError, LookupError):
        pass
    # Assume Latin-1 (behaviour before 3.7.1)
    return six.text_type(text, "latin-1"), 'latin-1-guessed'

def encode(text, orig_coding):
    """
    Function to encode a text.
    @param text text to encode (string)
    @param orig_coding type of the original coding (string)
    @return encoded text and encoding
    """
    if orig_coding == 'utf-8-bom':
        return BOM_UTF8 + text.encode("utf-8"), 'utf-8-bom'

    # Try declared coding spec
    coding = get_coding(text)
    if coding:
        try:
            return text.encode(coding), coding
        except (UnicodeError, LookupError):
            raise RuntimeError("Incorrect encoding (%s)" % coding)
    if orig_coding and orig_coding.endswith('-default'):
        coding = orig_coding.replace("-default", "")
        try:
            return text.encode(coding), coding
        except (UnicodeError, LookupError):
            pass
    if orig_coding == 'utf-8-guessed':
        return text.encode('utf-8'), 'utf-8'

    # Try saving as ASCII
    try:
        return text.encode('ascii'), 'ascii'
    except UnicodeError:
        pass

    # Save as UTF-8 without BOM
    return text.encode('utf-8'), 'utf-8'

def to_text(value):
    """Convert a value to text"""
    value = six.text_type(value)
    for codec, aliases, language in CODECS:
        try:
            return value.decode(codec)
        except UnicodeError:
            pass
        except TypeError:
            break
    return value

def write(text, filename, encoding='utf-8', mode='wb'):
    """
    Write 'text' to file ('filename') assuming 'encoding'
    Return (eventually new) encoding
    """
    text, encoding = encode(text, encoding)
    with open(filename, mode) as textfile:
        textfile.write(text)
    return encoding

def writelines(lines, filename, encoding='utf-8', mode='wb'):
    """
    Write 'lines' to file ('filename') assuming 'encoding'
    Return (eventually new) encoding
    """
    return write(os.linesep.join(lines), filename, encoding, mode)

def read(filename, encoding='utf-8'):
    """
    Read text from file ('filename')
    Return text and encoding
    """
    text, encoding = decode( open(filename, 'rb').read() )
    return text, encoding

def readlines(filename, encoding='utf-8'):
    """
    Read lines from file ('filename')
    Return lines and encoding
    """
    text, encoding = read(filename, encoding)
    return text.split(os.linesep), encoding

# ------------- Force ------------------------
def smart_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
Returns a text object representing 's' -- unicode on Python 2 and str on
Python 3. Treats bytestrings using the 'encoding' codec.

If strings_only is True, don't convert (some) non-string-like objects.
"""
    return force_text(s, encoding, strings_only, errors)

def is_protected_type(obj):
    """Determine if the object instance is of a protected type.

Objects of protected types are preserved as-is when passed to
force_text(strings_only=True).
"""
    return isinstance(obj, six.integer_types + (type(None), float, Decimal,
        datetime.datetime, datetime.date, datetime.time))

def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
Similar to smart_text, except that lazy instances are resolved to
strings, rather than kept as lazy objects.

If strings_only is True, don't convert (some) non-string-like objects.
"""
    # Handle the common case first, saves 30-40% when s is an instance of
    # six.text_type. This function gets called often in that setting.
    if isinstance(s, six.text_type):
        return s
    if strings_only and is_protected_type(s):
        return s
    try:
        if not isinstance(s, six.string_types):
            if hasattr(s, '__unicode__'):
                s = s.__unicode__()
            else:
                if six.PY3:
                    if isinstance(s, bytes):
                        s = six.text_type(s, encoding, errors)
                    else:
                        s = six.text_type(s)
                else:
                    s = six.text_type(bytes(s), encoding, errors)
        else:
            # Note: We use .decode() here, instead of six.text_type(s, encoding,
            # errors), so that if s is a SafeBytes, it ends up being a
            # SafeText at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if isinstance(s, Exception):
            s = ' '.join([force_text(arg, encoding, strings_only,
                    errors) for arg in s])
    return s

def smart_bytes(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
Returns a bytestring version of 's', encoded as specified in 'encoding'.

If strings_only is True, don't convert (some) non-string-like objects.
"""
    return force_bytes(s, encoding, strings_only, errors)


def force_bytes(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
Similar to smart_bytes, except that lazy instances are resolved to
strings, rather than kept as lazy objects.

If strings_only is True, don't convert (some) non-string-like objects.
"""
    if isinstance(s, bytes):
        if encoding == 'utf-8':
            return s
        else:
            return s.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and (s is None or isinstance(s, int)):
        return s
    if not isinstance(s, six.string_types):
        try:
            if six.PY3:
                return six.text_type(s).encode(encoding)
            else:
                return bytes(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return b' '.join([force_bytes(arg, encoding, strings_only,
                        errors) for arg in s])
            return six.text_type(s).encode(encoding, errors)
    else:
        return s.encode(encoding, errors)

if six.PY3:
    smart_str = smart_text
    force_str = force_text
else:
    smart_str = smart_bytes
    force_str = force_bytes

smart_str.__doc__ = """\
Apply smart_text in Python 3 and smart_bytes in Python 2.

This is suitable for writing to sys.stdout (for instance).
"""

force_str.__doc__ = """\
Apply force_text in Python 3 and force_bytes in Python 2.
"""

#------------------------------------------------------------------------------
#  Functions for encoding and decoding bytes that come from
#  the *file system*.
#------------------------------------------------------------------------------
def from_fs(string):
    return six.text_type(string, FS_ENCODING)

def to_fs(string):
    """Return a string version of unic encoded using the file system encoding."""
    return smart_str(string, encoding = FS_ENCODING)
