#!/usr/bin/env python
# -*- coding: utf-8 -*-

VERSION = (0, 9, 6, 'alpha', 0)

def get_git_revision(path=None):
    import os, prymatex
    rev = None
    if path is None:
        path = prymatex.__path__[0]
    git_command = '(cd %s; git rev-parse --short HEAD)' % path

    pipe = None
    try:
        pipe   = os.popen(git_command)
        rev = pipe.read()
    finally:
        if pipe: pipe.close()
    if rev:
        return u'GIT-%s' % rev.strip()
    return u'GIT-unknown'

def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            version = '%s %s %s' % (version, VERSION[3], VERSION[4])
    git_rev = get_git_revision()
    if git_rev != u'GIT-unknown':
        version = "%s %s" % (version, git_rev)
    return version

#-----------------------------------
# METADATA
#-----------------------------------
__prj__ = "prymatex"
__author__ = "The Prymatex Team"
__mail__ = "team at prymatex dot org"
__url__ = "http://www.prymatex.org"
__source__ = "http://ninja-ide.googlecode.com"
__license__ = "GPL3"
__version__ = get_version() # Dynamically calculate the version
if u'GIT' in __version__:
    __version__ = ' '.join(__version__.split(' ')[:-1])
    
#-----------------------------------
# DOC
#-----------------------------------
"""A PyQt4 based TextMate clone"""
