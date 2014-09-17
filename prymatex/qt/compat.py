#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from prymatex.qt import QtWidgets

#===============================================================================
# Wrappers around QFileDialog static methods
#===============================================================================

def getExistingDirectory(parent=None, caption='', basedir='',
                         options=QtWidgets.QFileDialog.ShowDirsOnly):
    """Wrapper around QtWidgets.QFileDialog.getExistingDirectory static method
    Compatible with PyQt >=v4.4 (API #1 and #2) and PySide >=v1.0"""
    # Calling QFileDialog static method
    if sys.platform == "win32":
        # On Windows platforms: redirect standard outputs
        _temp1, _temp2 = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = None, None
    try:
        result = QtWidgets.QFileDialog.getExistingDirectory(parent, caption, basedir,
                                                  options)
    finally:
        if sys.platform == "win32":
            # On Windows platforms: restore standard outputs
            sys.stdout, sys.stderr = _temp1, _temp2
    if not isinstance(result, str):
        # PyQt API #1
        result = str(result)
    return result

def _qfiledialog_wrapper(attr, parent=None, caption='', basedir='',
                         filters='', selectedfilter='', options=None):
    if options is None:
        options = QtWidgets.QFileDialog.Options(0)
    if isinstance(filters, (tuple, list)):
        filters = ";;".join(filters)
    try:
        # PyQt <v4.6 (API #1)
        from prymatex.qt import QtCore
    except ImportError:
        # PySide or PyQt >=v4.6
        QtCore.QString = None  
    tuple_returned = True
    try:
        # PyQt >=v4.6
        func = getattr(QtWidgets.QFileDialog, attr+'AndFilter')
    except AttributeError:
        # PySide or PyQt <v4.6
        func = getattr(QtWidgets.QFileDialog, attr)
        if QtCore.QString is not None:
            selectedfilter = QtCore.QString()
            tuple_returned = False
    
    # Calling QFileDialog static method
    if sys.platform == "win32":
        # On Windows platforms: redirect standard outputs
        _temp1, _temp2 = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = None, None
    try:
        result = func(parent, caption, basedir,
                      filters, selectedfilter, options)
    except TypeError:
        # The selectedfilter option (`initialFilter` in Qt) has only been 
        # introduced in Jan. 2010 for PyQt v4.7, that's why we handle here 
        # the TypeError exception which will be raised with PyQt v4.6
        # (see Issue 960 for more details)
        result = func(parent, caption, basedir, filters, options)
    finally:
        if sys.platform == "win32":
            # On Windows platforms: restore standard outputs
            sys.stdout, sys.stderr = _temp1, _temp2
            
    # Processing output
    if tuple_returned:
        # PySide or PyQt >=v4.6
        output, selectedfilter = result
    else:
        # PyQt <v4.6 (API #1)
        output = result
    if hasattr(QtCore, "QString"):
        # PyQt API #1: conversions needed from QString/QStringList
        selectedfilter = str(selectedfilter)
        if isinstance(output, QtCore.QString):
            # Single filename
            output = str(output)
        else:
            # List of filenames
            output = [str(fname) for fname in output]
            
    # Always returns the tuple (output, selectedfilter)
    return output, selectedfilter

def getOpenFileName(parent=None, caption='', basedir='', filters='',
                    selectedfilter='', options=None):
    """Wrapper around QtWidgets.QFileDialog.getOpenFileName static method
    Returns a tuple (filename, selectedfilter) -- when dialog box is canceled,
    returns a tuple of empty strings
    Compatible with PyQt >=v4.4 (API #1 and #2) and PySide >=v1.0"""
    return _qfiledialog_wrapper('getOpenFileName', parent=parent,
                                caption=caption, basedir=basedir,
                                filters=filters, selectedfilter=selectedfilter,
                                options=options)

def getOpenFileNames(parent=None, caption='', basedir='', filters='',
                     selectedfilter='', options=None):
    """Wrapper around QtWidgets.QFileDialog.getOpenFileNames static method
    Returns a tuple (filenames, selectedfilter) -- when dialog box is canceled,
    returns a tuple (empty list, empty string)
    Compatible with PyQt >=v4.4 (API #1 and #2) and PySide >=v1.0"""
    return _qfiledialog_wrapper('getOpenFileNames', parent=parent,
                                caption=caption, basedir=basedir,
                                filters=filters, selectedfilter=selectedfilter,
                                options=options)

def getSaveFileName(parent=None, caption='', basedir='', filters='',
                    selectedfilter='', options=None):
    """Wrapper around QtWidgets.QFileDialog.getSaveFileName static method
    Returns a tuple (filename, selectedfilter) -- when dialog box is canceled,
    returns a tuple of empty strings
    Compatible with PyQt >=v4.4 (API #1 and #2) and PySide >=v1.0"""
    return _qfiledialog_wrapper('getSaveFileName', parent=parent,
                                caption=caption, basedir=basedir,
                                filters=filters, selectedfilter=selectedfilter,
                                options=options)

if __name__ == '__main__':
    from prymatex.utils.qthelpers import qapplication
    app = qapplication()
    print(repr(getExistingDirectory()))
    print(repr(getOpenFileName(filters='*.py;;*.txt')))
    print(repr(getOpenFileNames(filters='*.py;;*.txt')))
    print(repr(getSaveFileName(filters='*.py;;*.txt')))
    sys.exit()
