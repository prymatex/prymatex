#!/usr/bin/env python

from prymatex.utils import osextra

def attributes(path):
    if path:
        revPath = [ p.replace(" ", "_") for p in osextra.path.fullsplit(path) ] + ['rev-path', 'attr']
        return ".".join(revPath[::-1])
    else:
        return 'attr.untitled'
