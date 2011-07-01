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

URL = 'http://www.prymatex.org'
AUTHOR = ('Diego Marcos van Haaster',
          'Nahuel Defosse',
          'Pablo Petenello' )
AUTHOR_EMAIL = ('diegomvh (at) gmail', 
                'nahuel (dto) defosse (at) gmail',
                'locurask (at) gmail' )

DESCRIPTION = """A PyQt4 based TextMate clone"""
LONG_DESCRIPTION = ("""
+-------+
|.....  |   Prymatex %(doc)s
|...    |   
|...... |   Version: %(version)s
+-------+.py

Website: %(website)s
Author/s:
%(authors)s

For more information use the -h option
""" % dict(doc = DESCRIPTION, version = get_version(),
           website = URL, 
           authors = '\n'.join(['\t%s' % a for a in AUTHOR]),
           )).strip()