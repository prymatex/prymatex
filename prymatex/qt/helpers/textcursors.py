#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

def textcursor_to_tuple(cursor):
    """Convert QKeyEvent instance into a tuple"""
    return (cursor.selectionStart(), cursor.selectionEnd())
    
