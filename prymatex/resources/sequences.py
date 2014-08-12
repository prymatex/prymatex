#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from prymatex.qt import QtGui
from prymatex.qt.helpers import keybinding

from prymatex.resources.base import getResource, setResource, getSection, removeSection

from prymatex.utils import text

class ContextSequence(namedtuple("ContextSequence", "context name default description")):
    __slots__ = ()
    def key(self):
        sec = keybinding(self.name)
        if sec.isEmpty():
            keystr = getResource(self.fullName(), 'Sequences')
            sec = QtGui.QKeySequence.fromString(keystr)
        if sec.isEmpty():
            sec = QtGui.QKeySequence.fromString(self.default)
        return sec

    def setKey(self, keystr):
        setResource('Sequences', '%s.%s' % (self.context, self.name), keystr)

    def fullName(self):
        return '%s.%s' % (self.context, self.name)

def get_sequence(context, name, default = None, description = None):
    """Get keyboard sequence"""
    return ContextSequence(context, name, default, description or text.camelcase_to_text(name))
    
def iter_sequences():
    """Iterate over keyboard shortcuts"""
    for option, value in getSection('Sequences').items():
        context, name = option.split(".", 1)
        yield context, name, value

def remove_deprecated_sequences(data):
    """Remove deprecated sequences"""
    source = 'Sequences'
    options = [('%s.%s' % (context, name)).lower() for (context, name) in data]
    for option, _ in CONF.items(section, raw=CONF.raw):
        if option not in options:
            CONF.remove_option(section, option)
            if len(CONF.items(section, raw=CONF.raw)) == 0:
                CONF.remove_section(section)

def reset_sequences():
    """Reset keyboard shortcuts to default values"""
    removeSection('Sequences')
