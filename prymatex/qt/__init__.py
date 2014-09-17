#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

os.environ.setdefault('QT_API', 'pyqt4')
assert os.environ['QT_API'] in ('pyqt4', 'pyside')

API = os.environ['QT_API']
API_NAME = {'pyqt4': 'PyQt4', 'pyqt5': 'PyQt5', 'pyside': 'PySide'}[API]

qt_version_str = pyqt4_version_str = pyqt5_version_str = sip_version_str = pyside_version_str = ""

if API == 'pyqt4':
    try:
        # Force API to #2
        import sip
        for obj in ['QDate', 'QTime', 'QDateTime', 'QUrl', 'QTextStream', 'QVariant', 'QString']:
            try:
                sip.setapi(obj, 2)
            except AttributeError:
                # PyQt < v4.6: in future version, we should warn the user
                # that PyQt is outdated and won't be supported by Prymatex
                pass
        from PyQt4.QtCore import qVersion, PYQT_VERSION_STR
        pyqt4_version_str = PYQT_VERSION_STR
        qt_version_str = qVersion()
        import sipconfig
        sip_version_str = sipconfig.Configuration().sip_version_str
    except ImportError as ex:
        sip_version_str = 'unknown'
        # Switching to PySide
        API = os.environ['QT_API'] = 'pyside'
        API_NAME = 'PySide'
    else:
        pyqt4_version_info = tuple(pyqt4_version_str.split('.')+['final', 1])
        is_old_pyqt4 = pyqt4_version_str.startswith(('4.4', '4.5', '4.6', '4.7'))
        is_pyqt46 = pyqt4_version_str.startswith('4.6')
        API_NAME += (" (API v%d)" % sip.getapi('QString'))

if API == 'pyside':
    try:
        from PySide import __version__ as pyside_version_str
    except ImportError:
        print("Prymatex requires PySide or PyQt to be installed")
        sys.exit(-1)
    else:
        is_old_pyqt4 = is_pyqt46 = False
