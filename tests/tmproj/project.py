#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import os, sys
sys.path.append(os.path.abspath('../..'))

from PyQt4 import QtCore, QtGui
from prymatex.utils.plist import readPlist
from pprint import pprint

if __name__ == "__main__":
    pprint(readPlist("untitled.tmproj.txt"))