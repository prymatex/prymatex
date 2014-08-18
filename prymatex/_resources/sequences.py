#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from prymatex.qt import QtGui
from prymatex.qt.helpers import keybinding

class ContextSequence(namedtuple("ContextSequence", "context name default description")):
    __slots__ = ()
    def is_empty(self):
        return self.key().isEmpty()

    def key(self):
        sec = keybinding(self.name)
        if sec.isEmpty():
            keystr = find_resource(self.full_name(), 'Sequences')
            sec = QtGui.QKeySequence.fromString(keystr or "")
        if sec.isEmpty():
            sec = QtGui.QKeySequence.fromString(self.default or "")
        return sec

    def full_name(self):
        return '%s.%s' % (self.context, self.name)
