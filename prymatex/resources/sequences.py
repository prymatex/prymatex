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
        sequence = keybinding(self.name)
        if sequence.isEmpty():
            keystr = self.resource.find_source(self.fullName(), 'Shortcuts')
            sequence = QtGui.QKeySequence.fromString(keystr or "")
        if sequence.isEmpty():
            sequence = QtGui.QKeySequence.fromString(self.default or "")
        return sequence

    def setKeySequence(self, sequence):
        shortcuts = self.resource.setdefault('Shortcuts', {})
        shortcuts[self.fullName()] = sequence.toString()

    def fullName(self):
        return '%s.%s' % (self.context, self.name)
