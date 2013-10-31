#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui

from prymatex.resources.loader import getResource

def get_shortcut(context, name, default = None):
    """Get keyboard shortcut (key sequence string)"""
    shortcut = getResource('%s.%s' % (context, name), 'Shortcuts')
    if shortcut is None:
        return default
    return shortcut

def set_shortcut(context, name, keystr):
    """Set keyboard shortcut (key sequence string)"""
    CONF.set('shortcuts', '%s.%s' % (context, name), keystr)
    
def iter_shortcuts():
    """Iterate over keyboard shortcuts"""
    for option in CONF.options('shortcuts'):
        context, name = option.split(".", 1)
        yield context, name, get_shortcut(context, name)

def remove_deprecated_shortcuts(data):
    """Remove deprecated shortcuts (shortcuts in CONF but not registered)"""
    section = 'shortcuts'
    options = [('%s.%s' % (context, name)).lower() for (context, name) in data]
    for option, _ in CONF.items(section, raw=CONF.raw):
        if option not in options:
            CONF.remove_option(section, option)
            if len(CONF.items(section, raw=CONF.raw)) == 0:
                CONF.remove_section(section)

def reset_shortcuts():
    """Reset keyboard shortcuts to default values"""
    CONF.remove_section('shortcuts')