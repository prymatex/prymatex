#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core.components.base import PMXBaseWidgetComponent

__all__ = ["PMXBaseStatusBar"]

class PMXBaseStatusBar(PMXBaseWidgetComponent):    
    def acceptEditor(self, editor):
        return False
