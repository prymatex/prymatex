#!/usr/bin/env python

from prymatex.utils import osextra

def ensurePath(path, name, suffix = 0):
    """Return a safe path, ensure not exists"""
    if suffix == 0 and not os.path.exists(path % name):
        return path % name
    else:
        newPath = path % (name + "_" + six.u(suffix))
        if not os.path.exists(newPath):
            return newPath
        else:
            return ensurePath(path, name, suffix + 1)

def attributes(path):
    if path:
        revPath = [ p.replace(" ", "_") for p in osextra.fullsplit(path) ]
        revPath.extend(['rev-path', 'attr'])
        return ".".join(revPath)
    else:
        return 'attr.untitled'
