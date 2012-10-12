#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if os.environ['QT_API'] == 'pyqt':
    from PyQt4.QtWebKit import *
else:
    from PySide.QtWebKit import *