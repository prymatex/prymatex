#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

os.environ.setdefault('QT_API', 'pyside')
assert os.environ['QT_API'] in ('pyqt', 'pyside')

API = os.environ['QT_API']
API_NAME = {'pyqt': 'PyQt4', 'pyside': 'PySide'}[API]

qt_version_str = pyqt_version_str = sip_version_str = pyside_version_str = ""

if API == 'pyqt':
    # Force QString, QVariant, ... API to #2
    import sip
    try:
        for obj in ['QDate', 'QTime', 'QDateTime', 'QUrl', 'QTextStream', 'QVariant', 'QString']:
            sip.setapi(obj, 2)
    except AttributeError:
        # PyQt < v4.6: in future version, we should warn the user 
        # that PyQt is outdated and won't be supported by Prymatex
        pass
    try:
        from PyQt4.QtCore import QT_VERSION_STR as qt_version_str
        from PyQt4.pyqtconfig import Configuration
        cfg = Configuration()
        sip_version_str = cfg.sip_version_str
        pyqt_version_str = cfg.pyqt_version_str
        del cfg
    except ImportError as ex:
        print(ex)
        # Switching to PySide
        API = os.environ['QT_API'] = 'pyside'
        API_NAME = 'PySide'
    else:
        pyqt_version_info = tuple(pyqt_version_str.split('.')+['final', 1])
        is_old_pyqt = pyqt_version_str.startswith(('4.4', '4.5', '4.6', '4.7'))
        is_pyqt46 = pyqt_version_str.startswith('4.6')
        import sip
        try:
            API_NAME += (" (API v%d)" % sip.getapi('QString'))
        except AttributeError:
            pass

if API == 'pyside':
    try:
        from PySide import __version__ as pyside_version_str
    except ImportError:
        raise ImportError("Prymatex requires PySide or PyQt to be installed")
    else:
        is_old_pyqt = is_pyqt46 = False
