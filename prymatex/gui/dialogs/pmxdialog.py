#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import sys
import plistlib
import zmq

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.utils.importlib import import_module, import_from_directory

class PMXDialogSystem(QtCore.QObject):
    def __init__(self, application):
        QtCore.QObject.__init__(self)
        self.application = application
        self.socket = self.application.zmqSocket(zmq.REP, "Dialog")
        self.socket.readyRead.connect(self.socketReadyRead)
    
    def socketReadyRead(self):
        command = self.socket.recv_pyobj()
        name = command.get("name")
        args = command.get("args", [])
        kwargs = command.get("kwargs", {})
        
        print args, kwargs
        #TODO: Filtro todo lo que sea None asumo que las signaturas de los metodos ponene los valores por defecto
        # esto tendria que ser controlado de una mejor forma
        kwargs = dict(filter(lambda (key, value): value != None, kwargs.iteritems()))
        
        method = getattr(self, name)
        method(*args, **kwargs)

    def _load_window(self, moduleName, directory):
        try:
            module = import_from_directory(directory, moduleName) if directory is not None else import_module(moduleName)
            loadFunction = getattr(module, 'load')
            loadFunction(self.application)
        except (ImportError, AttributeError), reason:
            #TODO: Manejar estos errores
            raise reason

    def sendResult(self, value = None):
        value = str(value) if value is not None else "ok"
        #Si tengo error retorno en lugar de result un error con { "code": <numero>, "message": "Cadena de error"}
        print "retorno", value        
        self.socket.send_pyobj({ "result": value })
        
    def async_window(self, nibPath, **kwargs):
        print "async_window: ", nibPath, kwargs
        directory = os.path.dirname(nibPath)
        name = os.path.basename(nibPath)
        self._load_window(name, directory)
        self.sendResult("1234")
    
    def tooltip(self, content, format = "text", transparent = False):
        self.application.currentEditor().showMessage(content)
        self.sendResult()
    
    def menu(self, plist):
        data = plistlib.readPlistFromString(plist)
        def sendSelectedIndex(index):
            self.sendResult(plistlib.writePlistToString({"selectedIndex": index}))
        self.application.currentEditor().showFlatPopupMenu(data["menuItems"], sendSelectedIndex)

    def popup(self, suggestions, returnChoice = False, caseInsensitive = True, alreadyTyped = "", staticPrefix = "", additionalWordCharacters = ""):
        suggestions = plistlib.readPlistFromString(suggestions)
        self.application.currentEditor().showCompleter(suggestions["suggestions"], alreadyTyped = alreadyTyped, caseInsensitive = caseInsensitive)
        self.sendResult()
    
    def defaults(self, args):
        print "defaults: ", args
        return True
    
    def images(self, plist):
        data = plistlib.readPlistFromString(plist)
        for name, path in data["register"].iteritems():
            resources.registerImagePath(name, path)
        self.sendResult()
    
    def alert(self, args):
        print "alert: ", args
        return True
    
    def debug(self, *args, **kwargs):
        print args, kwargs
        self.sendResult()