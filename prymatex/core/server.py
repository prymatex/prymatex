#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import sys
import plistlib
import zmq
from xml.parsers.expat import ExpatError

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.core.plugin import PMXBaseComponent
from prymatex.utils.importlib import import_module, import_from_directory

class PrymatexServer(QtCore.QObject, PMXBaseComponent):
    def __init__(self, application):
        QtCore.QObject.__init__(self)
        
        self.dialogs = {}
        self.instances = {}

        #Create socket
        self.socket = self.application.zmqSocket(zmq.REP, "Server")
        self.socket.readyRead.connect(self.socketReadyRead)
    
    def socketReadyRead(self):
        command = self.socket.recv_pyobj()
        name = command.get("name")
        kwargs = command.get("kwargs", {})
        
        #TODO: Filtro todo lo que sea None asumo que las signaturas de los metodos ponene los valores por defecto
        # esto tendria que ser controlado de una mejor forma
        kwargs = dict(filter(lambda (key, value): value != None, kwargs.iteritems()))
        
        self.logger.debug("Server Recv --> Method: %s, Arguments: %s" % (name, kwargs))
        method = getattr(self, name)
        try:
            method(**kwargs)
        except Exception, reason:
            self.sendResult({"error": {"code": -1, "message": reason.message}})
            raise reason

    def loadDialogClass(self, moduleName, directory):
        module = import_from_directory(directory, moduleName) if directory is not None else import_module(moduleName)
        dialogClass = getattr(module, 'dialogClass')
        self.application.populateComponent(dialogClass)
        return dialogClass
        
    def createDialogInstance(self, dialogClass, mainWindow, async = False):
        instance = dialogClass(mainWindow)
        self.application.settings.configure(instance)
        instance.initialize(mainWindow)
        if async:
            instanceId = id(instance)
            self.instances[instanceId] = instance
            return (instance, instanceId)
        return instance

    def dialogInstance(self, instanceId):
        return self.instances[instanceId]
        
    def sendResult(self, value = None):
        if value is None:
            value = ""
        if isinstance(value, int):
            value = str(value)
        if isinstance(value, dict):
            value = plistlib.writePlistToString(value)
        #Si tengo error retorno en lugar de result un error con { "code": <numero>, "message": "Cadena de error"}  
        #Ensure Unicode encode
        result = unicode(value).encode("utf-8")
        self.logger.debug("Server Send --> Result: %s" % (result))
        self.socket.send(result)
        
    def async_window(self, **kwargs):
        try:
            parameters = plistlib.readPlistFromString(kwargs["parameters"])
        except ExpatError:
            parameters = {}
        directory = os.path.dirname(kwargs["guiPath"])
        name = os.path.basename(kwargs["guiPath"])
        dialogClass = self.loadDialogClass(name, directory)
        instance, instanceId = self.createDialogInstance(dialogClass, self.application.mainWindow, async = True)
        instance.setParameters(parameters)
        instance.show()
        self.sendResult(instanceId)
    
    def update_window(self, **kwargs):
        try:
            parameters = plistlib.readPlistFromString(kwargs["parameters"])
        except ExpatError:
            parameters = {}
        instance = self.dialogInstance(int(kwargs["token"]))
        instance.setParameters(parameters)
        self.sendResult()

    def close_window(self, **kwargs):
        try:
            parameters = plistlib.readPlistFromString(kwargs["parameters"])
        except ExpatError:
            parameters = {}
        instance = self.dialogInstance(int(kwargs["token"]))
        instance.close()
        self.sendResult()

    def wait_for_input(self, **kwargs):
        try:
            parameters = plistlib.readPlistFromString(kwargs["parameters"])
        except ExpatError:
            parameters = {}
        instance = self.dialogInstance(int(kwargs["token"]))
        self.sendResult()

    def modal_window(self, **kwargs):
        try:
            parameters = plistlib.readPlistFromString(kwargs["parameters"])
        except ExpatError:
            parameters = {}
        directory = os.path.dirname(kwargs["guiPath"])
        name = os.path.basename(kwargs["guiPath"])
        dialogClass = self.loadDialogClass(name, directory)
        instance = self.createDialogInstance(dialogClass, self.application.mainWindow)
        instance.setParameters(parameters)
        value = instance.execModal()
        self.sendResult({"result": value})

    def tooltip(self, message = "", format = "text", transparent = False):
        try:
            data = plistlib.readPlistFromString(message)
            if data is not None:
                message = data[format]
        except ExpatError, reason:
            pass
        message = message.strip()
        if message:
            self.application.currentEditor().showMessage(message)
        self.sendResult()
    
    def menu(self, **kwargs):
        try:
            parameters = plistlib.readPlistFromString(kwargs["parameters"])
        except ExpatError:
            parameters = {}
            
        def sendSelectedIndex(index):
            if index != -1:
                self.sendResult({"selectedIndex": index})
            else:
                self.sendResult({})
            
        if "menuItems" in parameters:
            self.application.currentEditor().showFlatPopupMenu(parameters["menuItems"], sendSelectedIndex)

    def popup(self, suggestions = "", returnChoice = False, caseInsensitive = True, alreadyTyped = "", staticPrefix = "", additionalWordCharacters = ""):
        suggestions = plistlib.readPlistFromString(suggestions)
        self.application.currentEditor().showCompleter(suggestions["suggestions"], source = "external", alreadyTyped = alreadyTyped, caseInsensitive = caseInsensitive)
        self.sendResult()
    
    def defaults(self, **kwargs):
        return True
    
    def images(self, parameters = ""):
        data = plistlib.readPlistFromString(parameters)
        for name, path in data["register"].iteritems():
            resources.registerImagePath(name, path)
        self.sendResult()
    
    def alert(self, **kwargs):
        self.sendResult()
    
    def open(self, **kwargs):
        self.application.handleUrlCommand(kwargs["url"])
        self.sendResult()

    def debug(self, **kwargs):
        print kwargs
        self.sendResult()
