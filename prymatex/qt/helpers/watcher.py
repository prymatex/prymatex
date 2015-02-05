#!/usr/bin/env python

from prymatex.qt.extensions import FileSystemWatcher

CREATED = FileSystemWatcher.CREATED
DELETED = FileSystemWatcher.DELETED
RENAMED = FileSystemWatcher.RENAMED
CHANGED = FileSystemWatcher.CHANGED

_FileSystemWatcher = FileSystemWatcher()

CALLBACKS = {
}

def _on_fileChanged(path):
    print("Cambio", path)
    flags = CHANGED
    if not os.path.exists(path):
        flags |= DELETED
    for f, callback in CALLBACKS.get(path, []):
        if f | flags:
            callback(path, flags)

def _on_directoryChanged(path):
    pass

_FileSystemWatcher.fileChanged.connect(_on_fileChanged)
_FileSystemWatcher.directoryChanged.connect(_on_directoryChanged)

def on(flags, path, callback):
    CALLBACKS.setdefault(path, []).append((flags, callback))
    _FileSystemWatcher.addPath(path)

def on_change(path, callback):
    on(CHANGED, path, callback)
    
def on_delete(path, callback):
    on(DELETED, path, callback)
