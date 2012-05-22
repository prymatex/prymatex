# -*- coding: utf-8 -*-
# Copyright © 2011 by Vinay Sajip. All rights reserved. See accompanying LICENSE.txt for details.
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui
QT_VERSION_STR = QtCore.QT_VERSION_STR
PYQT_VERSION_STR = QtCore.PYQT_VERSION_STR
WRAPPER = 'PyQt'
Qt = QtCore.Qt
