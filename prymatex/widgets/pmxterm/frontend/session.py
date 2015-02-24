#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import ast
import signal

from prymatex.qt import QtCore

class Session(QtCore.QObject):
    readyRead = QtCore.pyqtSignal()
    screenReady = QtCore.pyqtSignal(list)
    finished = QtCore.pyqtSignal(int)
    
    def __init__(self, backend, width=80, height=24):
        QtCore.QObject.__init__(self, backend)
        
        self.backend = backend
        self.backend.finished.connect(lambda status, session = self: session.finished.emit(status))

        #Session Id
        self._session_id = "%s-%s" % (time.time(), id(self))
        
        self._width = width
        self._height = height
        self._started = False
        self._state = 'stop'
        self._pid = None
        
    def message(self, message):
        self._state = message['state']
        if self._state == 'alive':
            self.screenReady.emit(message['screen'])
        elif self._state == 'dead':
            print("Termino session")
            self.finished.emit(0)
        else:
            self.readyRead.emit()
        return True
        
    def sid(self):
        return self._session_id

    def resize(self, width, height):
        self._width = width
        self._height = height
        if self._started:
            self.keepalive()

    def start(self, *largs):
        args = [self._session_id, self._width, self._height]
        if largs:
            args.extend(largs)
        self.backend.execute("proc_keepalive", args)
        self._started = True
        return self._started

    def close(self):
        self.backend.execute("proc_bury", [self._session_id])
    
    stop = close

    def is_alive(self):
        return self._state == 'alive'

    def keepalive(self):
        self.backend.execute("proc_keepalive", [self._session_id, self._width, self._height])

    def dump(self):
        if self.is_alive():
            self.backend.execute("proc_dump", [self._session_id])

    def write(self, data):
        if self.is_alive():
            self.backend.execute("proc_write", [self._session_id, data])
    
    def info(self):
        self.backend.execute("session_info", [self._session_id])
