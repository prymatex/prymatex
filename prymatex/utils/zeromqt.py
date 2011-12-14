import zmq
from zmq import *

from PyQt4 import QtCore

class ZeroMQTContext(QtCore.QObject):
    def __init__(self, ioThreads = 1, parent = None):
        QtCore.QObject.__init__(self, parent)
        self.zmq_context = zmq.Context(ioThreads)
        if not self.zmq_context:
            pass
    
    def __getattr__(self, name):
        return getattr(self.zmq_context, name)
    
    def socket(self, socketType):
        if self.zmq_context.closed:
            raise zmq.ZMQError(zmq.ENOTSUP)
        return ZeroMQTSocket(self, socketType)
        
class ZeroMQTSocket(QtCore.QObject):
    readyRead = QtCore.pyqtSignal()
    readyWrite = QtCore.pyqtSignal()
    
    def __init__(self, context, socketType):
        QtCore.QObject.__init__(self, context)
        self.zmq_socket = context.zmq_context.socket(socketType)
        self.fd = self.zmq_socket.getsockopt(zmq.FD)
        self.readNotifier = QtCore.QSocketNotifier(self.fd, QtCore.QSocketNotifier.Read, self)
        self.readNotifier.activated.connect(self.notifierActivity)
        self.writeNotifier = QtCore.QSocketNotifier(self.fd, QtCore.QSocketNotifier.Write, self)
        self.writeNotifier.activated.connect(self.notifierActivity)
    
    def notifierActivity(self, value):
        print value
        self.readNotifier.setEnabled(False)
        self.writeNotifier.setEnabled(False)
        events = self.getsockopt(zmq.EVENTS)
        if events & zmq.POLLIN:
            self.readyRead.emit()
        if events & zmq.POLLOUT:
            self.readyWrite.emit()
        if events & zmq.POLLERR:
            pass

    def __getattr__(self, name):
        zmqSocketMethod = getattr(self.zmq_socket, name)
        def decorate(*args, **kwargs):
            returnValue = zmqSocketMethod(*args, **kwargs)
            self.readNotifier.setEnabled(True)
            self.writeNotifier.setEnabled(True)
            return returnValue
        return decorate
