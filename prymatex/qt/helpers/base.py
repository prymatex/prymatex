#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re

from prymatex.qt import QtCore, QtGui
from prymatex.utils import text

# Local import
import prymatex

# &Text Button name -> %{prefix}TextButtonName%{sufix}
text2objectname = lambda source, sufix = "", prefix = "": \
    prefix + text.to_alphanumeric(text.text_to_camelcase(source)) + sufix

def qapplication(translate=True):
    """Return QApplication instance creates it if it doesn't already exist"""
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication([])
        # Set Application name for Gnome 3 (https://groups.google.com/forum/#!topic/pyside/24qxvwfrRDs)
        app.setApplicationName(prymatex.__name__.title())
    if translate:
        install_translator(app)
    return app

def file_uri(fname):
    """Select the right file uri scheme according to the operating system"""
    if os.name == 'nt':
        # Local file
        if re.search(r'^[a-zA-Z]:', fname):
            return 'file:///' + fname
        # UNC based path
        else:
            return 'file://' + fname
    else:
        return 'file://' + fname

QT_TRANSLATOR = None
def install_translator(qapp):
    """Install Qt translator to the QApplication instance"""
    global QT_TRANSLATOR
    if QT_TRANSLATOR is None:
        qt_translator = QtCore.QTranslator()
        if qt_translator.load("qt_" + QtCore.QLocale.system().name(),
                      QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)):
            QT_TRANSLATOR = qt_translator # Keep reference alive
    if QT_TRANSLATOR is not None:
        qapp.installTranslator(QT_TRANSLATOR)
