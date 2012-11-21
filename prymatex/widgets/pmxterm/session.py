#!/usr/bin/env python

import sys
import zmq
import time

from prymatex.qt import QtCore

from prymatex.utils.zeromqt import ZmqSocket

class Session(QtCore.QObject):
    _sock = None
    readyRead = QtCore.pyqtSignal()
    
    @classmethod
    def close_all(cls):
        pass
        #cls.__send("stop", [])

    @classmethod
    def __send(cls, command, args):
        Session._sock.send_pyobj({"command": command, "args": args})
        return Session._sock.recv_pyobj()
    

    def __init__(self, connection, notifier, parent = None, width=80, height=24):
        QtCore.QObject.__init__(self, parent)
        if not Session._sock:
            Session._sock = ZmqSocket(zmq.REQ, self)
            Session._sock.connect(connection)
        
        #Session Id
        self._session_id = "%s-%s" % (time.time(), id(self))
        
        # Session subscriber
        self._subs = ZmqSocket(zmq.SUB, self)
        self._subs.readyRead.connect(self.subs_readyRead)
        self._subs.subscribe(self._session_id)
        self._subs.connect(notifier)
        
        self._width = width
        self._height = height
        self._started = False
        

    def subs_readyRead(self):
        sid = self._subs.recv()[0]
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