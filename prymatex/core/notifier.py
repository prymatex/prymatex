#!/usr/bin/env python

import os
from prymatex.qt import QtCore

NONE = 0
CREATED = 1<<0
DELETED = 1<<1
RENAMED = 1<<2
CHANGED = 1<<3

_FileSystemWatcher = None

WATCHS = {
}

PATHSCREATED = set()

class Watch(object):
    __slots__ = ('path', 'mask', 'callback', 'dir', 'skip')

    def __init__(self, path, mask, callback):
        self.path = path
        self.mask = mask
        self.callback = callback
        self.dir = os.path.isdir(self.path)
        self.skip = False

    def __call__(self, flags):
        if not self.skip and flags & self.mask:
            self.callback(self.path, flags)
        elif self.skip:
            self.skip = False

def _on_fileChanged(path):
    watchs = WATCHS.get(path, [])
    flags = CHANGED
    if not os.path.exists(path):
        flags |= DELETED
    for watch in watchs:
        watch(flags)

def _on_directoryChanged(path):
    watchs = WATCHS.get(path, [])
    flags = CHANGED
    if not os.path.exists(path):
        flags |= DELETED
    for p in os.listdir(path):
        if os.path.join(path, p) in PATHSCREATED:
            flags = CREATED
            path = os.path.join(path, p)
            break
    for watch in watchs:
        watch(flags)

def start_notifier():
    global _FileSystemWatcher
    _FileSystemWatcher = QtCore.QFileSystemWatcher()
    _FileSystemWatcher.fileChanged.connect(_on_fileChanged)
    _FileSystemWatcher.directoryChanged.connect(_on_directoryChanged)

def watch(path, mask, callback):
    watch = Watch(path, mask, callback)
    WATCHS.setdefault(watch.path, []).append(watch)
    _FileSystemWatcher.addPath(watch.path)
    return watch

def unwatch(watch):
    WATCHS.setdefault(watch.path, []).remove(watch)
    _FileSystemWatcher.removePath(watch.path)
