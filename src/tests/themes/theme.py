#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import plistlib
from pprint import pprint
#import ipdb

class Theme(object):
    def __init__(self, **kwargs):
        pass

    @classmethod
    def load(cls, path):
        string = open(path, 'r').read()
        data = plistlib.readPlistFromString(string.decode('cp1252').encode('utf8'))
        #ipdb.set_trace()    
        pprint(data)
        return Theme(data)

def main():
    paths = glob.glob('./Themes/*.tmTheme')
    for path in paths:
        print path
        theme = Theme.load(os.path.abspath(path))
        return

if __name__ == '__main__':
    main()