import prymatex
import os
import re

def get_git_revision(path=None):
    rev = None
    if path is None:
        path = prymatex.__path__[0]
    git_command = '(cd %s; git rev-parse --short HEAD)' % path

    try:
        rev = os.system(git_command)
    except IOError:
        pass
    if rev:
        return u'GIT-%s' % rev
    return u'GIT-unknown'
