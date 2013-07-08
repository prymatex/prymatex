#!/usr/bin/env python

from prymatex.utils import osextra

def attributes(filePath, projectDirectory = None):
    if filePath:
        revPath = [ p.replace(" ", "_") for p in osextra.path.fullsplit(filePath) ] + ['rev-path', 'attr']
        return [ ".".join(revPath[::-1]) ]
    else:
        return [ 'attr.untitled' ]
