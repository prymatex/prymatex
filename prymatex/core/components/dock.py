#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core.components.base import (PrymatexComponentWidget, PrymatexAddon)

class PrymatexDock(PrymatexComponentWidget):
    SEQUENCE = None
    ICON = None
    PREFERED_AREA = QtCore.Qt.RightDockWidgetArea

    def __init__(self, *args, **kwargs):
        super(PrymatexDock, self).__init__(*args, **kwargs)

#========================================
# BASE ADDON
#========================================
class PrymatexDockAddon(PrymatexAddon):
    def __init__(self, **kwargs):
        super(PrymatexDockAddon, self).__init__(**kwargs)
        self.dock = kwargs.get("parent")
