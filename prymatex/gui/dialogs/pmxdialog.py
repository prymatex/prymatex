#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import plistlib
import zmq

from prymatex import resources

from PyQt4 import QtCore, QtGui

PORT = 4612

class PMXDialogSystem(QtCore.QObject):
    def __init__(self, application):
        QtCore.QObject.__init__(self)
        self.application = application
        self.socket = self.application.zmqContext.socket(zmq.REP)
        self.socket.bind('tcp://127.0.0.1:%s' % PORT)
        self.socket.readyRead.connect(self.socketReadyRead)
    
    def socketReadyRead(self):
        command = self.socket.recv_pyobj()
        name = command.get("name")
        args = command.get("args", [])
        kwargs = command.get("kwargs", {})
        
        #TODO: Filtro todo lo que sea None asumo que las signaturas de los metodos ponene los valores por defecto
        # esto tendria que ser controlado de una mejor forma
        kwargs = dict(filter(lambda (key, value): value != None, kwargs.iteritems()))
        
        method = getattr(self, name)
        method(*args, **kwargs)

    def sendResult(self, value = None):
        value = str(value) if value is not None else "ok"
        #Si tengo error retorno en lugar de result un error con { "code": <numero>, "message": "Cadena de error"}
        self.socket.send_pyobj({ "result": value })
        
    def async_window(self, *args, **kwargs):
        print "async_window: ", args, kwargs
        self.sendResult("1234")
    
    def tooltip(self, args):
        print "Tooltip: ", options, args
        return True
    
    def menu(self, plist):
        #TODO: Instanciar un completer y pasarle los valores
        data = plistlib.readPlistFromString(plist)
        def sendSelectedIndex(index):
            self.sendResult(plistlib.writePlistToString({"selectedIndex": index}))
        self.application.currentEditor().showFlatPopupMenu(data["menuItems"], sendSelectedIndex)

    def popup(self, suggestions, returnChoice = False, caseInsensitive = True, alreadyTyped = "", staticPrefix = "", additionalWordCharacters = ""):
        suggestions = plistlib.readPlistFromString(suggestions)
        self.application.currentEditor().showCompleter(suggestions["suggestions"], alreadyTyped = alreadyTyped, caseInsensitive = caseInsensitive)
        self.sendResult()
    
    def defaults(self, args):
        print "defaults: ", options, args
        return True
    
    def images(self, plist):
        data = plistlib.readPlistFromString(plist)
        for name, path in data["register"].iteritems():
            resources.registerImagePath(name, path)
        self.sendResult()
    
    def alert(self, args):
        print "alert: ", options, args
        return True
    
    def debug(self, *args, **kwargs):
        print args, kwargs
        self.sendResult()