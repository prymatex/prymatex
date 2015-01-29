#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui
from prymatex.qt.helpers import keybinding

from prymatex.utils import text as textutils

class ContextKeySequence(QtGui.QKeySequence):
    def __init__(self, context, name, default=None, description=None):
        self._context = context
        self._name = name
        self._default = keybinding(name)
        self._description = description or textutils.camelcase_to_text(name)
        if self._default.isEmpty() and default:
            self._default = QtGui.QKeySequence.fromString(default)
        super(ContextKeySequence, self).__init__(self._default)

    def isDefault(self):
        return self == self._default

    def update(self, sequence):
        self.swap(QtGui.QKeySequence(sequence))

    def reset(self):
        self.update(self._default)

    def name(self):
        return self._name
        
    def default(self):
        return self._default

    def description(self):
        return self._description

    def context(self):
        return self._context

    def identifier(self):
        return '%s.%s' % (self._context, self._name)

