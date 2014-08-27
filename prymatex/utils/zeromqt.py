#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import zmq
from zmq import (FD, LINGER, IDENTITY, SUBSCRIBE, UNSUBSCRIBE, EVENTS,
                POLLIN, POLLOUT, POLLERR, NOBLOCK, ZMQError, EAGAIN,
                REP, REQ, SUB)
                
from prymatex.qt import QtCore

class ZmqContext(object):
    self_=None
    def __init__(self, iothreads, defaultLinger):
        assert not ZmqContext.self_
        self._linger=defaultLinger
        self._context=zmq.Context(iothreads)

    def __del__(self): self._context.term()

    def majorVersion(self): return zmq.zmq_version_info()[0]

    def minorVersion(self): return zmq.zmq_version_info()[1]

    def patchVersion(self): return zmq.zmq_version_info()[2]

    def version(self): return zmq.zmq_version()

    def linger(self): return self._linger

    def setLinger(self, msec): self._linger=msec

    @staticmethod
    def instance(iothreads=4, defaultLinger=0):
        if not ZmqContext.self_: 
            ZmqContext.self_=ZmqContext(iothreads, defaultLinger)
        return ZmqContext.self_
        
class ZmqSocket(QtCore.QObject):
    readyRead = QtCore.Signal()
    readyWrite = QtCore.Signal()
    def __init__(self, _type, parent=None):
        QtCore.QObject.__init__(self, parent)

        ctx=ZmqContext.instance()
        self._socket=ctx._context.socket(_type)
        self.setLinger(ctx.linger())

        fd=self._socket.getsockopt(FD)
        self._notifier=QtCore.QSocketNotifier(fd, QtCore.QSocketNotifier.Read, self)
        self._notifier.activated.connect(self.activity)

    def __del__(self): self._socket.close()

    def setIdentity(self, name): self._socket.setsockopt(IDENTITY, name)

    def identity(self): return self._socket.getsockopt(IDENTITY)

    def setLinger(self, msec): self._socket.setsockopt(LINGER, msec)

    def linger(self): return self._socket.getsockopt(LINGER)

    def subscribe(self, _filter): self._socket.setsockopt(SUBSCRIBE, _filter)

    def unsubscribe(self, _filter): self._socket.setsockopt(UNSUBSCRIBE, _filter)

    def bind(self, addr): self._socket.bind(addr)

    def bind_to_random_port(self, addr): return self._socket.bind_to_random_port(addr)

    def connect(self, addr): self._socket.connect(addr)

    def activity(self):
        flags=self._socket.getsockopt(EVENTS)
        if flags&POLLIN: 
            self.readyRead.emit()
        elif flags&POLLOUT: 
            self.readyWrite.emit()
        elif flags&POLLERR: 
            pass
            #print "ZmqSocket.activity(): POLLERR"
        else:
            pass
            #print "ZmqSocket.activity(): fail"

    def _recv(self, flags=NOBLOCK):
        try: _msg=self._socket.recv(flags=flags)
        except ZMQError as e:
            if e.errno==EAGAIN: return None
            else: raise ZMQError(e)
        else: return _msg

    def _recv_multipart(self, flags=NOBLOCK):
        try: _msg=self._socket.recv_multipart(flags=flags)
        except ZMQError as e:
            if e.errno==EAGAIN: return None
            else: raise ZMQError(e)
        else: return _msg
    
    def recv(self):
        _return = ""
        while 1:
            _msg = self._recv()
            if not _msg:
                break
            _return += _msg
        return _return   
    
    def recv_multipart(self):
        _return = []
        while 1:
            _msg = self._recv_multipart()
            if not _msg:
                break
            _return = _msg
        return _return
    
    def recv_pyobj(self): return self._socket.recv_pyobj()
    
    def recv_json(self): return self._socket.recv_json()
    
    def send(self, _msg): return self._socket.send(_msg)
    
    def send_pyobj(self, _msg): return self._socket.send_pyobj(_msg)
    
    def send_json(self, _msg): return self._socket.send_json(_msg)
    
    def send_multipart(self, _msg): return self._socket.send_multipart(_msg)
    
