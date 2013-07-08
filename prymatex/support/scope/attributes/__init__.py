#!/usr/bin/env python

from functools import reduce

from .system import attributes as system_attributes
from .scm import attributes as scm_attributes
from .path import attributes as path_attributes
from .build import attributes as build_attributes

def attributes(filePath, projectDirectory = None):
    return tuple(reduce(lambda s1, s2: s1 + s2, 
        map(lambda func: func(filePath, projectDirectory),
            [ path_attributes, system_attributes, scm_attributes, build_attributes]),
        []))
