#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import zmq
import time
import json
import ast

from prymatex.qt import QtCore

from prymatex.utils.zeromqt import ZmqSocket

LOCAL_BACKEND_SCRIPT = os.path.join(os.path.dirname(__file__), "backend", "main.py")

class Session(QtCore.QObject):
    readyRead = QtCore.pyqtSignal()
    
    def __init__(self, parent = None, width=80, height=24):
        QtCore.QObject.__init__(self, parent)
        
        #Session Id
        self._session_id = "%s-%s" % (time.time(), id(self))
        
        self._width = width
        self._height = height
        self._started = False

    def connect(self, shell_address, pub_address):
        self._shell = ZmqSocket(zmq.REQ, self)
        self._shell.connect(shell_address)
        
        # Session subscriber
        self._pub = ZmqSocket(zmq.SUB, self)
        self._pub.readyRead.connect(self.subs_readyRead)
        self._pub.subscribe(self._session_id)
        self._pub.connect(pub_address)

    def __send(self, command, args):
        self._shell.send_pyobj({"command": command, "args": args})
        return self._shell.recv_pyobj()
    
    def subs_readyRead(self):
        sid = self._pub.recv()[0]
        if sid == self._session_id:
            self.readyRead.emit()
        
    def resize(self, width, height):
        self._width = width
        self._height = height
        if self._started:
            self.keepalive()


    def start(self, command):
        self._started = self.__send("proc_keepalive", [self._session_id, self._width, self._height, command])
        return self._started

    def close(self):
        return self.__send("proc_bury", [self._session_id])
    
    stop = close

    def is_alive(self):
        return self.__send("is_session_alive", [self._session_id])

        
    def keepalive(self):
        return self.__send("proc_keepalive", [self._session_id, self._width, self._height])


    def dump(self):
        if self.keepalive():
            return self.__send("proc_dump", [self._session_id])


    def write(self, data):
        if self.keepalive():
            return self.__send("proc_write", [self._session_id, data])


    def last_change(self):
        return self.__send("last_session_change", [self._session_id])
        
    
    def pid(self):
        return self.__send("session_pid", [self._session_id])
        
    def info(self):
        return self.__send("session_info", [self._session_id])
        
class Backend(QtCore.QObject):
    def __init__(self, name, multiplexer_address, notifier_address, process = None, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.name = name
        self.process = process   # If backend is local
        self.multiplexer_address = multiplexer_address
        self.notifier_address = notifier_address
        self.multiplexer = ZmqSocket(zmq.REQ, self)
        self.multiplexer.connect(multiplexer_address)
        
    def close(self):
        self.multiplexer.send_pyobj({"command": "stop", "args": []})
        self.multiplexer.recv_pyobj()
        if self.process is not None:
            self.process.kill()
            self.process.waitForFinished()

    def session(self):
        session = Session(self)
        session.connect(self.multiplexer_address, self.notifier_address)
        return session

class BackendManager(QtCore.QObject):
    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.backends = []
    
    def closeAll(self):
        for backend in self.backends:
            backend.close()
    
    def backend(self, name, connection, process = None):
        data = ast.literal_eval(connection)
        backend = Backend(name, data["multiplexer"], data["notifier"], process = process, parent = self)
        self.backends.append(backend)
        return backend
        
    def localBackend(self, workingDirectory = None):
        process = QtCore.QProcess(self)
        
        if workingDirectory:
            process.setWorkingDirectory(workingDirectory)
        
        process.finished.connect(self.backendFinished)

        process.start(sys.executable, [LOCAL_BACKEND_SCRIPT, "-t", "tcp"])    
        process.waitForReadyRead()
        lines = str(process.readAllStandardOutput()).decode("utf-8").splitlines()
        return self.backend("local", lines[-1], process)

    def backendFinished(self):
        # emitir una señal de que se murio uno backend
        pass
