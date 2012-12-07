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
    screenReady = QtCore.pyqtSignal(tuple)
    
    def __init__(self, backend, width=80, height=24):
        QtCore.QObject.__init__(self, backend)
        
        self.backend = backend
        
        #Session Id
        self._session_id = "%s-%s" % (time.time(), id(self))
        
        self._width = width
        self._height = height
        self._started = False
        
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
        return self.backend.execute("session_pid", [self._session_id])
        
    def info(self):
        return self.backend.execute("session_info", [self._session_id])
        
class Backend(QtCore.QObject):
    def __init__(self, name, multiplexer_address, notifier_address, process = None, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.name = name
        self.process = process   # If backend is local
        
        if self.process is not None:
            self.process.finished.connect(self.backend_finished)
            self.process.readyReadStandardError.connect(self.backend_readyReadStandardError)
            self.process.readyReadStandardOutput.connect(self.backend_readyReadStandardOutput)
        
        self.sessions = {}
        
        self.multiplexer = ZmqSocket(zmq.REQ, self)
        self.multiplexer.connect(multiplexer_address)
        
        self.notifier = ZmqSocket(zmq.SUB, self)
        self.notifier.readyRead.connect(self.notifier_readyRead)
        self.notifier.subscribe("") #All
        self.notifier.connect(notifier_address)

    #------------ Process Signals
    def backend_finished(self):
        # emitir una señal de que se murio uno backend
        print "se murio el backend"
        
    def backend_readyReadStandardError(self):
        print str(self.process.readAllStandardError()).decode("utf-8")
        
    def backend_readyReadStandardOutput(self):
        print str(self.process.readAllStandardOutput()).decode("utf-8")

    def execute(self, command, args = None):
        if args is None:
            args = []
        self.multiplexer.send_pyobj({"command": command, "args": args})
        return self.multiplexer.recv_pyobj()

    def notifier_readyRead(self):
        message = self.notifier.recv_multipart()
        if len(message) % 2 == 0:
            for sid, payload in [message[x: x + 2] for x in xrange(0, len(message), 2)]:
                if sid in self.sessions:
                    try:
                        self.sessions[sid].screenReady.emit(ast.literal_eval(payload))
                    except:
                        self.sessions[sid].readyRead.emit()
        else:
            print "algo esta mal con", data
        
            
    def close(self):
        self.execute("stop")
        if self.process is not None:
            self.process.kill()
            self.process.waitForFinished()

    def platform(self):
        return self.execute("platform")
        
    def session(self):
        session = Session(self)
        self.sessions[session.sid()] = session
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
        
    def localBackend(self, workingDirectory = None, protocol = None, address = None):
        if protocol is None:
            protocol = 'ipc' if sys.platform.startswith('linux') else 'tcp'
        args = [LOCAL_BACKEND_SCRIPT, "-t", protocol]
        
        process = QtCore.QProcess(self)
        
        if workingDirectory:
            process.setWorkingDirectory(workingDirectory)
            
        if address is not None:
            args.extend(["-a", address])
        
        process.start(sys.executable, args)    
        dataAvailable  = process.waitForReadyRead(2000)
        if dataAvailable:
            lines = str(process.readAllStandardOutput()).decode("utf-8").splitlines()
            return self.backend("local", lines[-1], process)
        else:
            print str(process.readAllStandardError()).decode("utf-8")
