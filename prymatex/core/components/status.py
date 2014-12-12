#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core.components.base import PrymatexComponentWidget

class PrymatexStatusBar(PrymatexComponentWidget):
    def __init__(self, **kwargs):
        super(PrymatexStatusBar, self).__init__(**kwargs)
        #self.window = kwargs.get("parent")

    def acceptEditor(self, editor):
        return False
