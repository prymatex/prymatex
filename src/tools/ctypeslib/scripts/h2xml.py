#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os.path import dirname, join
sys.path.append(join(dirname(__file__), '..'))
from ctypeslib.h2xml import main

if __name__ == "__main__":
    sys.exit(main())
