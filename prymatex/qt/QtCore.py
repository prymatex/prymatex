#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if os.environ['QT_API'] == 'pyqt4':
    from PyQt4.QtCore import *
    from PyQt4.Qt import QCoreApplication
    from PyQt4.QtCore import pyqtSignal as Signal
    from PyQt4.QtCore import pyqtSlot as Slot
    from PyQt4.QtCore import pyqtProperty as Property
    from PyQt4.QtCore import QT_VERSION_STR as __version__
else:
    import PySide.QtCore
    __version__ = PySide.QtCore.__version__
    from PySide.QtCore import *
    
Qt.MatchRole = Qt.UserRole + 1
Qt.Key_Any = 0
