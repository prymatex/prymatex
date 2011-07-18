#!/usr/bin/env python
# coding: utf-8

import sys
from xml.etree.ElementTree import ElementTree

DEFAULT_RESOURCE_FILE = 'resources.qrc'

def main(argv = sys.argv[1:]):
    args = argv[1:]
    
    tree = ElementTree()
    tree.parse(DEFAULT_RESOURCE_FILE)
    print tree


if __name__ == "__main__":
    sys.exit(main())