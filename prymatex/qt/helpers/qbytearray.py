#!/usr/bin/env python

from prymatex.qt import QtCore
from prymatex.utils import six

def qbytearray_to_text(qbytearray):
    return six.text_type(qbytearray.data()).decode())

def qbytearray_to_hex(qbytearray):
    return six.text_type(qbytearray.toHex().data()).decode())

def hex_to_qbytearray(hexadecimal):
    return QtCore.QByteArray.fromHex(hexadecimal.encode())
