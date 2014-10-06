#!/usr/bin/env python

from prymatex.qt import QtCore

def qt_int(data):
    return QtCore.QVariant(data).toInt()[0]
