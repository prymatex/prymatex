#!/usr/bin/env python
import sys
from os.path import abspath,join
ctypeslib_path = abspath(join(__file__, '..', '..'))
sys.path.append(ctypeslib_path)
from ctypeslib.h2xml import main

if __name__ == "__main__":
    sys.exit(main())
