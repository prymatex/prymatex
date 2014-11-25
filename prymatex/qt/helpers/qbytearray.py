#!/usr/bin/env python

from prymatex.qt import QtCore
from prymatex.utils import encoding

def qbytearray_to_hex(qbytearray):
    return encoding.force_text(qbytearray.toHex().data())

def hex_to_qbytearray(hexadecimal):
    return QtCore.QByteArray.fromHex(hexadecimal)
