#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.qt import QtGui, QtCore

__fileIconProvider = QtGui.QFileIconProvider()

def get_file_type(path):
    return __fileIconProvider.type(QtCore.QFileInfo(path))
