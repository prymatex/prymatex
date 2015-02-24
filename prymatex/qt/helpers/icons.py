#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.utils import text as textutils

__all__ = [ "combine_icons", "get_std_icon", "get_path_icon", "get_type_icon", "text_to_iconname" ]

_FileIconProvider = QtWidgets.QFileIconProvider()

def text_to_iconname(value, prefix="", sufix=""):
    """&Text Button name -> %{prefix}-text-button-name-%{sufix}"""
    if prefix:
        value = "%s %s" % (prefix, value)
    if sufix:
        value = "%s %s" % (value, sufix)
    return textutils.slugify(value.replace("&", ""))

def combine_icons(icon1, icon2, scale = 1):
    newIcon = QtGui.QIcon()
    sizes = icon1.availableSizes()
    if not sizes:
        sizes = [ QtCore.QSize(16, 16), QtCore.QSize(22, 22), QtCore.QSize(32, 32), QtCore.QSize(48, 48) ]
    for size in sizes:
        pixmap1 = icon1.pixmap(size)
        pixmap2 = icon2.pixmap(size)
        pixmap2 = pixmap2.scaled(pixmap1.width() * scale, pixmap1.height() * scale)
        result = QtGui.QPixmap(size)
        result.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(result)
        painter.drawPixmap(0, 0, pixmap1)
        painter.drawPixmap(pixmap1.width() - pixmap2.width(), pixmap1.height() - pixmap2.height(), pixmap2)
        painter.end()
        newIcon.addPixmap(result)
    return newIcon

def get_std_icon(name):
    if not name.startswith('SP_'):
        name = 'SP_' + name
    standardIconName = getattr(QtWidgets.QStyle, name, None)
    if standardIconName is not None:
        return QtWidgets.QWidget().style().standardIcon(standardIconName)
    return QtGui.QIcon()

def get_path_icon(path):
    return _FileIconProvider.icon(QtCore.QFileInfo(path))
    
def get_type_icon(_type):
    return _FileIconProvider.icon(_type)
    
def get_type(path):
    return _FileIconProvider.type(QtCore.QFileInfo(path))

