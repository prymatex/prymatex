#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex.core.components.base import PMXBaseComponent

__all__ = ["PMXBaseStatusBar"]

class PMXBaseStatusBar(PMXBaseComponent):    
    def acceptEditor(self, editor):
        return False
