#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if os.environ['QT_API'] == 'pyqt4':
    from PyQt4.Qt import QKeySequence, QTextCursor
    from PyQt4.QtGui import *
elif os.environ['QT_API'] == 'pyqt5':
    from PyQt5.Qt import QKeySequence, QTextCursor
    from PyQt5.QtGui import *
else:
    from PySide.QtGui import *
