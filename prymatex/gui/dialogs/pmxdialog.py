#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import sys
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
        
        print args, kwargs
        #TODO: Filtro todo lo que sea None asumo que las signaturas de los metodos ponene los valores por defecto
        # esto tendria que ser controlado de una mejor forma
        kwargs = dict(filter(lambda (key, value): value != None, kwargs.iteritems()))
        
        method = getattr(self, name)
        method(*args, **kwargs)

    def _import_module(self, name):
        __import__(name)
        return sys.modules[name]
    
    def _load_window(self, moduleName, directory):
        old_syspath = sys.path[:]
        try:
            if directory is not None:
                sys.path.insert(1, directory)
            module = self._import_module(moduleName)
            module.load(self.application)
        except Exception as reason:
            print(reason)
        finally:
            sys.path = old_syspath

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