#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
import time
import json
import ast
import signal
import tempfile
import functools

from prymatex.qt import QtNetwork, QtCore
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
    error = QtCore.pyqtSignal(int)
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal(int)
    stateChanged = QtCore.pyqtSignal(int)

    def __init__(self, name, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.name = name
        self.sessions = {}
        self._state = self.NotRunning
        self._protocol = 'unix' if sys.platform.startswith('linux') else 'inet'
        self._address = None
        self.multiplexer = None
        self.notifier = None

    def _set_state(self, state):
        self._state = state
        self.stateChanged.emit(state)

    def state(self):
        return self._state

    def setProtocol(self, protocol):
        self._protocol = protocol

    def protocol(self):
        return self._protocol
        
    def setAddress(self, address):
        self._address = address
        if address.startswith('/'):
            self.setProtocol('unix')
        else:
            self.setProtocol('inet')

    def address(self):
        return self._address

    #------------ Sockets
    def startNotifier(self):
        if self.protocol() == 'unix':
            address = tempfile.mktemp(prefix="pmx")
            self.notifier = QtNetwork.QLocalServer(self)
            self.notifier.listen(address)
        else:
            self.notifier = QtNetwork.QTcpServer(self)
            self.notifier.listen()
            address = "%s:%d" % (
                self.notifier.serverAddress().toString(), self.notifier.serverPort()
            )
        self.notifier.newConnection.connect(self.on_notifier_newConnection)
        return address

    def startMultiplexer(self, address):
        if self.protocol() == 'unix':
            self.multiplexer = QtNetwork.QLocalSocket(self)
            self.multiplexer.connectToServer(address, QtCore.QIODevice.WriteOnly)
        else:
            self.multiplexer = QtNetwork.QTcpSocket(self)
            address, port = address.split(':')
            self.multiplexer.connectToHost(address, int(port), QtCore.QIODevice.WriteOnly)
        
    def execute(self, command, args=()):
        if not isinstance(args, (tuple, list)):
            args = [ args ]
        data = {"command": command, "args": args}
        self.multiplexer.write(json.dumps(data).encode(encoding.FS_ENCODING))
        self.multiplexer.flush()

    def on_notifier_newConnection(self):
        connection = self.notifier.nextPendingConnection()
        connection.readyRead.connect(functools.partial(self.socketReadyRead, connection))
        
    def socketReadyRead(self, connection):
        payload = encoding.from_fs(connection.readAll().data())
        for data in filter(lambda d: d, payload.split("\n\n")):
            message = json.loads(data)
            sid = message['sid']
            if sid in self.sessions:
                self.sessions[sid].message(message)
        
    def start(self):
        self.startMultiplexer(self.address())
        self.execute("setup_channel", self.startNotifier())
        self._set_state(self.Running)
        self.started.emit()
        
    def stop(self):
        self.execute("proc_buryall")
        self._set_state(self.NotRunning)

    def platform(self):
        return self.execute("platform")

    def session(self):
        session = Session(self)
        self.sessions[session.sid()] = session
        session.finished.connect(self.on_session_finished)
        return session

    @QtCore.Slot(int)
    def on_session_finished(self, value):
        session = self.sender()
        del self.sessions[session.sid()]
        session.deleteLater()
        if not self.sessions and self.state() == self.NotRunning:
            self.finished.emit(0)

class LocalBackend(Backend):
    def __init__(self, parent=None):
        Backend.__init__(self, 'local', parent)
        self.process = QtCore.QProcess(self)
        
    def start(self):
        self._set_state(self.Starting)
        args = [LOCAL_BACKEND_SCRIPT, "-t", self.protocol()]
        if self.address() is not None:
            args.extend(["-a", self.address()])

        def backend_start_readyReadStandardOutput():
            connection = encoding.from_fs(self.process.readAllStandardOutput()).splitlines()[1]
            connection = json.loads(connection)
            self.setAddress(connection['address'])
            self.process.readyReadStandardError.disconnect(backend_start_readyReadStandardError)
            self.process.readyReadStandardOutput.disconnect(backend_start_readyReadStandardOutput)
            self.process.readyReadStandardError.connect(self.backend_readyReadStandardError)
            self.process.readyReadStandardOutput.connect(self.backend_readyReadStandardOutput)
            self.process.finished.connect(self.backend_finished)
            self.process.error.connect(self.backend_error)
            super(LocalBackend, self).start()
    
        def backend_start_readyReadStandardError():
            print(encoding.from_fs(self.process.readAllStandardError()))
            self.process.readyReadStandardError.disconnect(backend_start_readyReadStandardError)
            self.process.readyReadStandardOutput.disconnect(backend_start_readyReadStandardOutput)
            self.error.emit(self.ReadError)
            self.finished.emit(-1)
            
        self.process.readyReadStandardError.connect(backend_start_readyReadStandardError)
        self.process.readyReadStandardOutput.connect(backend_start_readyReadStandardOutput)
        self.process.start(sys.executable, args)

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

class BackendManager(QtCore.QObject):
    def __init__(self, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.backends = []
    
    def stopAll(self):
        for backend in self.backends:
            if backend.state() == Backend.Running:
                backend.stop()
    
    def backend(self, address):
        backend = Backend(address, parent=self)
        backend.setAddress(address)
        self.backends.append(backend)
        return backend
        
    def localBackend(self, workingDirectory=None, protocol=None, address=None):
        backend = LocalBackend(self)
        
        if protocol is not None:
            backend.setProtocol(protocol)
        
        if workingDirectory:
            backend.setWorkingDirectory(workingDirectory)
            
        if address is not None:
            backend.setAddress(address)

        self.backends.append(backend)
        return backend
