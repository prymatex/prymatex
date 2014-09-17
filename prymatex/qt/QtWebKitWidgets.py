#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if os.environ['QT_API'] == 'pyqt4':
    from PyQt4.QtWebKit import *
elif os.environ['QT_API'] == 'pyqt5':
    from PyQt5.QtWebKitWidgets import *
else:
    from PySide.QtWebKit import *
