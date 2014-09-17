#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if os.environ['QT_API'] == 'pyqt4':
    from PyQt4.Qt import *

QWIDGETSIZE_MAX = 16777215
Key_Any = 0