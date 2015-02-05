#!/usr/bin/env python

#http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qfilesystemwatcher.html

from prymatex.qt import QtCore

class FileSystemWatcher(QtCore.QFileSystemWatcher):
    # ---------------- Constants
    CREATED = 1<<0
    DELETED = 1<<1
    RENAMED = 1<<2
    MOVED   = 1<<3
    CHANGED = 1<<4

    # ------------ Signals
    fileCreated = QtCore.Signal(str)
    fileDeleted = QtCore.Signal(str)
    fileRenamed = QtCore.Signal(str, str)
    directoryCreated = QtCore.Signal(str)
    directoryDeleted = QtCore.Signal(str)
    directoryRenamed = QtCore.Signal(str, str)

    # Generic Signal 
    fileSytemChanged = QtCore.Signal(str, int)

    def __init__(self):
        super(FileSystemWatcher, self).__init__()
        self.fileChanged.connect(self.on_fileChanged)
        self.directoryChanged.connect(self.on_directoryChanged)
        UNARY_SINGAL_CONSTANT_MAP = (
            (self.fileCreated, FileSystemWatcher.CREATED ),
            (self.fileDeleted, FileSystemWatcher.DELETED ),
            (self.fileChanged, FileSystemWatcher.CHANGED ),
            (self.directoryCreated, FileSystemWatcher.CREATED ),
            (self.directoryDeleted, FileSystemWatcher.DELETED ),
            (self.directoryChanged, FileSystemWatcher.CHANGED ),
        )
        BINARY_SINGAL_CONSTANT_MAP = (
            (self.fileRenamed, FileSystemWatcher.RENAMED ),
            (self.directoryRenamed, FileSystemWatcher.RENAMED ),                       
        )
        for signal, associatedConstant in UNARY_SINGAL_CONSTANT_MAP:
            signal.connect(lambda path, constant=associatedConstant: self.fileSytemChanged.emit(path, constant))
        for signal, associatedConstant in BINARY_SINGAL_CONSTANT_MAP:
            signal.connect(lambda _x, path, constant=associatedConstant: self.fileSytemChanged.emit(path, constant))

    def on_fileChanged(self, path):
        if not os.path.exists(path):
            self.fileDeleted.emit(path)

    def on_directoryChanged(self, path):
        if not os.path.exists(path):
            self.directoryDeleted.emit(path)
