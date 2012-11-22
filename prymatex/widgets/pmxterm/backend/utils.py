#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, locale, sys

PREFERRED_ENCODING = locale.getpreferredencoding()

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

def to_unicode_from_fs(string):
    """
    Return a unicode version of string decoded using the file system encoding.
    """
    if not isinstance(string, basestring): # string is a QString
        string = unicode(string.toUtf8(), 'utf-8')
    else:
        if not isinstance(string, unicode):
            try:
                unic = string.decode(FS_ENCODING)
            except (UnicodeError, TypeError):
                pass
            else:
                return unic
    return string
    
def get_home_dir():
    """
    Return user home directory
    """
    try:
        # expanduser() returns a raw byte string which needs to be
        # decoded with the codec that the OS is using to represent file paths.
        path = to_unicode_from_fs(os.path.expanduser('~'))
    except:
        path = ''
    for env_var in ('HOME', 'USERPROFILE', 'TMP'):
        if os.path.isdir(path):
            break
        # os.environ.get() returns a raw byte string which needs to be
        # decoded with the codec that the OS is using to represent environment
        # variables.
        path = to_unicode_from_fs(os.environ.get(env_var, ''))
    if path:
        return path
    else:
        raise RuntimeError('Please define environment variable $HOME')

def get_pmxterm_dir():
    path = os.path.join(get_home_dir(), ".config", "pmxterm")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

if __name__ == '__main__':
    print get_home_dir()