#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if os.environ['QT_API'] == 'pyqt4':
    from PyQt4.Qt import QKeySequence, QTextCursor
    from PyQt4.QtGui import *

elif os.environ['QT_API'] == 'pyqt5':
    from PyQt5.QtWidgets import *

else:
    from PySide.QtGui import *

#####################################################
# Monkey patching
#####################################################
QApplication._app__init__ = QApplication.__init__
QApplication.__init__ = lambda self, *largs, **kwargs: QApplication._app__init__(self, kwargs.get("argv", []))
