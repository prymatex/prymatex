# -*- coding: utf-8 -*-
# Copyright © 2011 by Vinay Sajip. All rights reserved. See accompanying LICENSE.txt for details.
try:
    import cPickle as pickle
except ImportError:
    import pickle
import logging
import select
import socket
import struct
import threading
try:
    import zmq
except ImportError:
    zmq = None

class BaseServer(object):   # mixin for common functionality

    allow_reuse_address = 1

    def __init__(self, handler, timeout):
        self._record_handler = handler
        self._stop = threading.Event()
        self.timeout = timeout
        self.formatter = logging.Formatter('%(asctime)s')

    def handle_record(self, record):
        self.formatter.format(record)
        self._record_handler(record)

    def serve_until_stopped(self):
        while not self._stop.isSet():
            rd, wr, ex = self.select()
            if rd:
                self.handle_request()
        self.server_close()

    def select(self):
        return select.select([self.socket.fileno()], [], [], self.timeout)

    def stop(self):
        self._stop.set()
#
# TCP receiver
#

from SocketServer import ThreadingTCPServer, StreamRequestHandler

class LogRecordStreamHandler(StreamRequestHandler):
    """
    Handler for a streaming logging request. It basically logs the record
    using whatever logging policy is configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while True:
            try:
                chunk = self.connection.recv(4)
                if len(chunk) < 4:
                    break
                slen = struct.unpack(">L", chunk)[0]
                chunk = self.connection.recv(slen)
                while len(chunk) < slen:
                    chunk = chunk + self.connection.recv(slen - len(chunk))
                obj = pickle.loads(chunk)
                record = logging.makeLogRecord(obj)
                self.server.handle_record(record)
            except socket.error, e:
                if type(e.args) != types.TupleType:
                    raise
                else:
                    errcode = e.args[0]
                    if errcode != RESET_ERROR:
                        raise
                    break

class LoggingTCPServer(ThreadingTCPServer, BaseServer):
    """
    A simple-minded TCP socket-based logging receiver suitable for test
    purposes.
    """

    def __init__(self, addr, handler, timeout=1):
        ThreadingTCPServer.__init__(self, addr, LogRecordStreamHandler)
        BaseServer.__init__(self, handler, timeout)

#
# UDP receiver
#

from SocketServer import ThreadingUDPServer, DatagramRequestHandler

class LogRecordDatagramHandler(DatagramRequestHandler):
    """
    Handler for a datagram logging request. It basically logs the record using
    whatever logging policy is configured locally.
    """
    def handle(self):
        chunk = self.packet
        slen = struct.unpack(">L", chunk[:4])[0]
        chunk = chunk[4:]
        assert len(chunk) == slen
        obj = pickle.loads(chunk)
        record = logging.makeLogRecord(obj)
        self.server.handle_record(record)

    def finish(self):
        pass

class LoggingUDPServer(ThreadingUDPServer, BaseServer):
    """
    A simple-minded UDP datagram-based logging receiver suitable for test
    purposes.
    """

    def __init__(self, addr, handler, timeout=1):
        ThreadingUDPServer.__init__(self, addr, LogRecordDatagramHandler)
        BaseServer.__init__(self, handler, timeout)

if zmq:
    class LoggingZMQServer(BaseServer):
        def __init__(self, addr, handler, timeout=1):
            BaseServer.__init__(self, handler, timeout)
            self.ctx = zmq.Context()
            self.socket = zmq.Socket(self.ctx, zmq.SUB)
            self.socket.setsockopt(zmq.SUBSCRIBE, '')
            self.socket.connect(addr)
        
        def select(self):
            return zmq.select([self.socket], [], [], self.timeout)
        
        def handle_request(self):
            data = pickle.loads(self.socket.recv())
            record = logging.makeLogRecord(data)
            self.handle_record(record)

        def server_close(self):
            self.socket.close()
