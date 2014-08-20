#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from prymatex.qt import QtGui
from prymatex.qt.helpers import keybinding
from prymatex.utils import text

from .base import find_resource, set_resource, get_section, del_section

class ContextSequence(namedtuple("ContextSequence", "context name default description")):
    __slots__ = ()
    def isEmpty(self):
        return self.key().isEmpty()

    def key(self):
        sec = keybinding(self.name)
        if sec.isEmpty():
            keystr = find_resource(self.fullName(), 'Sequences')
            sec = QtGui.QKeySequence.fromString(keystr or "")
        if sec.isEmpty():
            sec = QtGui.QKeySequence.fromString(self.default or "")
        return sec

    def setKey(self, keystr):
        set_resource('Sequences', '%s.%s' % (self.context, self.name), keystr)

    def fullName(self):
        return '%s.%s' % (self.context, self.name)

def get_sequence(context, name, default = None, description = None):
    """Get keyboard sequence"""
    return ContextSequence(context, name, default, description or text.camelcase_to_text(name))

def iter_sequences():
    """Iterate over keyboard shortcuts"""
    for option, value in get_section('Sequences').items():
        context, name = option.split(".", 1)
        yield context, name, value

def reset_sequences():
    """Reset keyboard shortcuts to default values"""
    del_section('Sequences')

# TODO Este codigo esta para ver
def remove_deprecated_sequences(data):
    """Remove deprecated sequences"""
    source = 'Sequences'
    options = [('%s.%s' % (context, name)).lower() for (context, name) in data]
    for option, _ in CONF.items(section, raw=CONF.raw):
        if option not in options:
            CONF.remove_option(section, option)
            if len(CONF.items(section, raw=CONF.raw)) == 0:
                CONF.remove_section(section)
