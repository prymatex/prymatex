#!/usr/bin/env python
from __future__ import unicode_literals

from .parser import parse_symbol
from . import types

class SymbolTransformation(object):
    def __init__(self, source):
        self.nodes = parse_symbol(source)

    def __str__(self):
        return ";".join(["%s" % node for node in self.nodes])

    def transform(self, text):
        for node in self.nodes:
            if isinstance(node, types.SymbolTransformationType):
                transformation = node.replace({}, variables = {node.name: text})
                if transformation:
                    return transformation
