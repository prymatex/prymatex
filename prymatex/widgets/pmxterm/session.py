#!/usr/bin/env python

import sys
import zmq
import time
import json

from PyQt4 import QtCore

from zeromqt import ZmqSocket

class Session(QtCore.QObject):
    readyRead = QtCore.pyqtSignal()
    
    @classmethod
    def close_all(cls):
        pass
        #cls.__send("stop", [])


    def __init__(self, parent = None, width=80, height=24):
        QtCore.QObject.__init__(self, parent)
        
        #Session Id
        self._session_id = "%s-%s" % (time.time(), id(self))
        
        self._width = width
        self._height = height
        self._started = False

    def connect(self, shell_address = None, pub_address = None, 
            connection_file = None):
        assert connection_file is not None or\
            (shell_address is not None and pub_address is not None ),\
            "No connection address or file"

        if connection_file is not None:
            with open(connection_file, 'r') as fdata:
                data = json.loads(fdata.read())
            shell_address = data["shell_address"]
            pub_address = data["pub_address"]
            
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
        return self.__send("proc_keepalive",
            [self._session_id, self._width, self._height, command])

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