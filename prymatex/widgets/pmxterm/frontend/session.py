#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import zmq
import time
import json
import ast
import signal

from PyQt4 import QtCore

class Session(QtCore.QObject):
    readyRead = QtCore.pyqtSignal()
    screenReady = QtCore.pyqtSignal(tuple)
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
        self._pid = None
        
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
        self._started = self.backend.execute("proc_keepalive", args)
        return self._started

    def close(self):
        return self.backend.execute("proc_bury", [self._session_id])
    
    stop = close

    def is_alive(self):
        return self.backend.execute("is_session_alive", [self._session_id])

        
    def keepalive(self):
        return self.backend.execute("proc_keepalive", [self._session_id, self._width, self._height])


    def dump(self):
        if self.keepalive():
            return self.backend.execute("proc_dump", [self._session_id])


    def write(self, data):
        if self.keepalive():
            return self.backend.execute("proc_write", [self._session_id, data])


    def last_change(self):
        return self.backend.execute("last_session_change", [self._session_id])
        
    
    def pid(self):
        if self._pid is None:
            self._pid = self.backend.execute("session_pid", [self._session_id])
        return self._pid
        
    def info(self):
        return self.backend.execute("session_info", [self._session_id])
