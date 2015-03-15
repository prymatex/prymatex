#!/usr/bin/env python

class Namespace(object):
    __slots__ = ('name', 'path', 'environment')
    def __init__(self, name, path):
        super(Namespace, self).__init__()
        self.name = name
        self.path = path
        self.environment = {}
        