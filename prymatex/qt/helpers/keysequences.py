#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui

def keybinding(attr):
    """Return keybinding"""
    ks = getattr(QtGui.QKeySequence, attr)
    return QtGui.QKeySequence.keyBindings(ks)[0]