#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import plistlib
import zmq

from prymatex import resources

from PyQt4 import QtCore

PORT = 4612

class PMXDialogSystem(QtCore.QObject):
    def __init__(self, parent = None):
        QtCore.QObject.__init__(self)
        self.application = parent
        self.socket = parent.zmqContext.socket(zmq.REP)
        self.socket.bind('tcp://127.0.0.1:%s' % PORT)
        self.socket.readyRead.connect(self.socketReadyRead)
    
    def socketReadyRead(self):
        command = self.socket.recv_pyobj()
        method = getattr(self, command["name"])
        value = method(*command["args"], **command["kwargs"])
        if value is None:
            value = ""
        self.socket.send_pyobj({ "status": "ok", "data": value })

    def nib(self, args):
        print "nib: ", options, args
        return True
    
    def tooltip(self, args):
        print "Tooltip: ", options, args
        return True
    
    def menu(self, plist):
        #TODO: Instanciar un completer y pasarle los valores
        data = plistlib.readPlistFromString(plist)
        print data, data["menuItems"]
        return plistlib.writePlistToString({})
            
    def popup(self, suggestions, returnChoice = False, caseInsensitive = True, alreadyTyped = "", staticPrefix = "", additionalWordCharacters = ""):
        suggestions = plistlib.readPlistFromString(suggestions)
        self.application.currentEditor().showCompleter(suggestions["suggestions"])
    
    def defaults(self, args):
        print "defaults: ", options, args
        return True
    
    def images(self, plist):
        data = plistlib.readPlistFromString(plist)
        for name, path in data["register"].iteritems():
            resources.registerImagePath(name, path)
    
    def alert(self, args):
        print "alert: ", options, args
        return True
    
    def debug(self, args):
        print args
        self.socket.send_pyobj({ "status": "ok", "data": ""})
