#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import plistlib
import zmq
from PyQt4 import QtCore

PORT = 4612

class PMXDialogSystem(QtCore.QObject):
    def __init__(self, parent = None):
        self.socket = parent.zmqContext.socket(zmq.REP)
        self.socket.bind('tcp://127.0.0.1:%s' % PORT)
        self.socket.readyRead.connect(self.socketReadyRead)
    
    def socketReadyRead(self):
        command = self.socket.recv_pyobj()
        print command
        method = getattr(self, command["name"])
        method(command["args"])

    def nib(self, options, args):
        print "nib: ", options, args
        return True
    
    def tooltip(self, options, args):
        print "Tooltip: ", options, args
        return True
    
    def menu(self, plist):
        #TODO: Instanciar un completer y pasarle los valores
        data = plistlib.readPlistFromString(plist)
        print data
        self.socket.send_pyobj({ "status": "ok", "data": plistlib.writePlistToString({})})
    
    def popup(self, options, args):
        print "popup: ", options, args
        return True
    
    def defaults(self, options, args):
        print "defaults: ", options, args
        return True
    
    def images(self, options, args):
        print "images: ", options, args
        return True
    
    def alert(self, options, args):
        print "alert: ", options, args
        return True
    
    def debug(self, options, args):
        print "debug: ", options, args
        return True
