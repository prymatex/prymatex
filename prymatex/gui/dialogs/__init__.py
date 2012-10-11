#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
    
from PyQt4 import QtGui

def getOpenFiles(directory):
    return QtGui.QFileDialog.getOpenFileNames(None, "Open Files", directory)

def getSaveFile(directory, name = "", title = "Save file", filters = []):
    filePath = os.path.join(directory, name) 
    
    filters = ";;".join(filters)
    name = QtGui.QFileDialog.getSaveFileName(None, title, filePath, filters)
    if name:
        return name

def getFileName(extensions = [], directory = None, parent = None):
    name, ok = QtGui.QInputDialog.getText(parent, "New file name", "<p>Please enter the new file name in</p><p>%s</p>" % directory)
    if ok:
        return name

def getDirectoryName(directory = None, parent = None):
    name, ok = QtGui.QInputDialog.getText(parent, "New directoy name", "<p>Please enter the new directoy name in</p><p>%s</p>" % directory)
    if ok:
        return name
        
#===============================================================================
# Wrappers around QFileDialog static methods
# Copyright © 2011 Pierre Raybaut
# Licensed under the terms of the MIT License
#===============================================================================

def getExistingDirectory(parent=None, caption='', basedir='',
                         options=QtGui.QFileDialog.ShowDirsOnly):
    """Wrapper around QtGui.QFileDialog.getExistingDirectory static method
    Compatible with PyQt >=v4.4 (API #1 and #2) and PySide >=v1.0"""
    # Calling QFileDialog static method
    if sys.platform == "win32":
        # On Windows platforms: redirect standard outputs
        _temp1, _temp2 = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = None, None
    try:
        result = QtGui.QFileDialog.getExistingDirectory(parent, caption, basedir,
                                                  options)
    finally:
        if sys.platform == "win32":
            # On Windows platforms: restore standard outputs
            sys.stdout, sys.stderr = _temp1, _temp2
    if not isinstance(result, basestring):
        # PyQt API #1
        result = unicode(result)
    return result

def _qfiledialog_wrapper(attr, parent=None, caption='', basedir='',
                         filters='', selectedfilter='', options=None):
    if options is None:
        options = QtGui.QFileDialog.Options(0)
    try:
        # PyQt <v4.6 (API #1)
        from spyderlib.qt.QtCore import QString
    except ImportError:
        # PySide or PyQt >=v4.6
        QString = None  # analysis:ignore
    tuple_returned = True
    try:
        # PyQt >=v4.6
        func = getattr(QtGui.QFileDialog, attr+'AndFilter')
    except AttributeError:
        # PySide or PyQt <v4.6
        func = getattr(QtGui.QFileDialog, attr)
        if QString is not None:
            selectedfilter = QString()
            tuple_returned = False
    
    # Calling QtGui.QFileDialog static method
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
    if QString is not None:
        # PyQt API #1: conversions needed from QString/QStringList
        selectedfilter = unicode(selectedfilter)
        if isinstance(output, QString):
            # Single filename
            output = unicode(output)
        else:
            # List of filenames
            output = [unicode(fname) for fname in output]
            
    # Always returns the tuple (output, selectedfilter)
    return output, selectedfilter

def getOpenFilename(parent=None, caption='', basedir='', filters='',
                    selectedfilter='', options=None):
    """Wrapper around QtGui.QFileDialog.getOpenFileName static method
    Returns a tuple (filename, selectedfilter) -- when dialog box is canceled,
    returns a tuple of empty strings
    Compatible with PyQt >=v4.4 (API #1 and #2) and PySide >=v1.0"""
    return _qfiledialog_wrapper('getOpenFileName', parent=parent,
                                caption=caption, basedir=basedir,
                                filters=filters, selectedfilter=selectedfilter,
                                options=options)

def getOpenFilenames(parent=None, caption='', basedir='', filters='',
                     selectedfilter='', options=None):
    """Wrapper around QtGui.QFileDialog.getOpenFileNames static method
    Returns a tuple (filenames, selectedfilter) -- when dialog box is canceled,
    returns a tuple (empty list, empty string)
    Compatible with PyQt >=v4.4 (API #1 and #2) and PySide >=v1.0"""
    return _qfiledialog_wrapper('getOpenFileNames', parent=parent,
                                caption=caption, basedir=basedir,
                                filters=filters, selectedfilter=selectedfilter,
                                options=options)

def getSaveFilename(parent=None, caption='', basedir='', filters='',
                    selectedfilter='', options=None):
    """Wrapper around QtGui.QFileDialog.getSaveFileName static method
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
    print repr(getExistingDirectory())
    print repr(getOpenFilename(filters='*.py;;*.txt'))
    print repr(getOpenFilenames(filters='*.py;;*.txt'))
    print repr(getSaveFilename(filters='*.py;;*.txt'))
    sys.exit()
