#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from prymatex.qt import QtGui
from prymatex.qt.helpers import keybinding

__all__ = ["ContextKeySequence"]

class ContextKeySequence(namedtuple("ContextKeySequence", "resource context name default description")):
    __slots__ = ()
    def isEmpty(self):
        return self.keySequence().isEmpty()

    def keySequence(self):
        sec = keybinding(self.name)
        if sec.isEmpty():
            keystr = self.resource.find_source(self.fullName(), 'Sequences')
            sec = QtGui.QKeySequence.fromString(keystr or "")
        if sec.isEmpty():
            sec = QtGui.QKeySequence.fromString(self.default or "")
        return sec

    def fullName(self):
        return '%s.%s' % (self.context, self.name)
