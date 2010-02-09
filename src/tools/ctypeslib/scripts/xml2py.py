#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, join
sys.path.append(join(dirname(__file__), '..'))
from ctypeslib.xml2py import main

if __name__ == "__main__":
    sys.exit(main())
