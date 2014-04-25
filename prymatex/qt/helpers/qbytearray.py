#!/usr/bin/env python

from prymatex.qt import QtCore

def qbytearray_to_text(qbytearray):
    return qbytearray.data()

def qbytearray_to_hex(qbytearray):
    return qbytearray.toHex().data()

def hex_to_qbytearray(hexadecimal):
    return QtCore.QByteArray.fromHex(hexadecimal)
