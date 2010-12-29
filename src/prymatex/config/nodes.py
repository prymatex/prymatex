#!/usr/bin/env python
#

from PyQt4.QtCore import QObject
from UserDict import UserDict

class ConfigNode(QObject,):
    '''
    Config node
    '''
    _parent = None

    def namespace(self):
        max_depth = 100
        while
    def __init__(self):
        pass

    def toJson(self, stream_or_name):
        pass

    def toPlist(self, stream_or_name):
        pass

    def A__setitem__(self, name, value):
        pass

    def A__getitem__(self, name):
        pass


if __name__ == "__main__":
    c = ConfigNode()
    c.pepe = 1
    c.tata = 2
    print c