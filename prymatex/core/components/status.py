#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core.components.base import PrymatexComponentWidget

class PrymatexStatusBar(PrymatexComponentWidget):    
    def acceptEditor(self, editor):
        return False
