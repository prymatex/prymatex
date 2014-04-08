#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import time
import json
import ast
import signal

from prymatex.qt import QtCore
from prymatex.utils import encoding

from .session import Session

LOCAL_BACKEND_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "main.py"))

class Backend(QtCore.QObject):
    # Errors of Backend
    FailedToStart = 0
    Crashed = 1
    Timedout = 2
    WriteError = 4
    ReadError = 3
    UnknownError = 5
    # ------------- States of Backend
    NotRunning = 0
    Starting = 1
    Running = 2
    # ------------- Signals
    error = QtCore.Signal(int)
    started = QtCore.Signal()
    finished = QtCore.Signal(int)
    stateChanged = QtCore.Signal(int)
    
    def __init__(self, name, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.name = name
        self.sessions = {}
        self._state = self.NotRunning

    def _set_state(self, state):
        self._state = state
        self.stateChanged.emit(state)

    def state(self):
        return self._state

    #------------ Sockets
    def startMultiplexer(self, address):
        import zmq
        from prymatex.utils.zeromqt import ZmqSocket
        self.multiplexer = ZmqSocket(zmq.REQ, self)
        self.multiplexer.connect(address)
    
    def startNotifier(self, address):
        import zmq
        from prymatex.utils.zeromqt import ZmqSocket
        self.notifier = ZmqSocket(zmq.SUB, self)
        self.notifier.readyRead.connect(self.notifier_readyRead)
        self.notifier.subscribe(b"") #All
        self.notifier.connect(address)
        
    def execute(self, command, args = None):
        if args is None:
            args = []
        self.multiplexer.send_pyobj({"command": command, "args": args})
        return self.multiplexer.recv_pyobj()

    def notifier_readyRead(self):
        message = self.notifier.recv_multipart()
        if len(message) % 2 == 0:
            for sid, payload in [message[x: x + 2] for x in range(0, len(message), 2)]:
                sid = sid.decode("utf-8")
                payload = payload.decode("utf-8")
                if sid in self.sessions:
                    try:
                        self.sessions[sid].screenReady.emit(ast.literal_eval(payload))
                    except:
                        self.sessions[sid].readyRead.emit()
        else:
            raise Exception("Session data error")

    def start(self):
        self._set_state(self.Running)
        self.started.emit()
        
    def close(self):
        self.execute("proc_buryall")
        self._set_state(self.NotRunning)
        self.finished.emit(0)

    def platform(self):
        return self.execute("platform")

    def session(self):
        session = Session(self)
        self.sessions[session.sid()] = session
        return session

class LocalBackend(Backend):
    def __init__(self, parent = None):
        Backend.__init__(self, 'local', parent)
        self.process = QtCore.QProcess(self)
        self.protocol = 'ipc' if sys.platform.startswith('linux') else 'tcp'
        self.address = None

    def start(self):
        self._set_state(self.Starting)
        args = [LOCAL_BACKEND_SCRIPT, "-t", self.protocol]
        if self.address is not None:
            args.extend(["-a", self.address])

        self.process.readyReadStandardError.connect(self.backend_start_readyReadStandardError)
        self.process.readyReadStandardOutput.connect(self.backend_start_readyReadStandardOutput)
        self.process.start(sys.executable, args)

    def close(self):
        Backend.close(self)
        os.kill(self.process.pid(), signal.SIGTERM)
        self.process.waitForFinished()
        
    #------------ Process Start Signal
    def backend_start_readyReadStandardOutput(self):
        connectionString = encoding.from_fs(self.process.readAllStandardOutput()).splitlines()[-1]
        data = ast.literal_eval(connectionString)
        self.startMultiplexer(data["multiplexer"])
        self.startNotifier(data["notifier"])
        self.process.readyReadStandardError.disconnect(self.backend_start_readyReadStandardError)
        self.process.readyReadStandardOutput.disconnect(self.backend_start_readyReadStandardOutput)
        self.process.readyReadStandardError.connect(self.backend_readyReadStandardError)
        self.process.readyReadStandardOutput.connect(self.backend_readyReadStandardOutput)
        self.process.finished.connect(self.backend_finished)
        self.process.error.connect(self.backend_error)
        self._set_state(self.Running)
        self.started.emit()

    def backend_start_readyReadStandardError(self):
        print(encoding.from_fs(self.process.readAllStandardError()))
        self.process.readyReadStandardError.disconnect(self.backend_start_readyReadStandardError)
        self.process.readyReadStandardOutput.disconnect(self.backend_start_readyReadStandardOutput)
        self.error.emit(self.ReadError)
        self.finished.emit(-1)

    #------------ Process Normal Signals
    def backend_finished(self):
        self.finished.emit(0)

    def backend_error(self, error):
        self.error.emit(error)

    def backend_readyReadStandardError(self):
        print(encoding.from_fs(self.process.readAllStandardError()))
    
    def backend_readyReadStandardOutput(self):
        print(encoding.from_fs(self.process.readAllStandardOutput()))
    
    # -------------- set backend process attrs and settings
    def setWorkingDirectory(self, directory):
        self.process.setWorkingDirectory(directory)

    def setProtocol(self, protocol):
        self.protocol = protocol

    def setAddress(self, address):
        self.address = address

class BackendManager(QtCore.QObject):
    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.backends = []
    
    def closeAll(self):
        for backend in self.backends:
            backend.close()
    
    def backend(self, name, connectionString):
        data = ast.literal_eval(connectionString)
        backend = Backend(name, parent = self)
        backend.startMultiplexer(data["multiplexer"])
        backend.startNotifier(data["notifier"])
        self.backends.append(backend)
        return backend
        
    def localBackend(self, workingDirectory = None, protocol = None, address = None):
        backend = LocalBackend(self)
        
        if protocol is not None:
            backend.setProtocol(protocol)
        
        if workingDirectory:
            backend.setWorkingDirectory(workingDirectory)
            
        if address is not None:
            backend.setAddress(address)

        self.backends.append(backend)
        return backend
