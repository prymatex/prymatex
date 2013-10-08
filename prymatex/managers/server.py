#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, sys
import zmq

from prymatex.qt import QtCore, QtGui
from prymatex.core import PMXBaseComponent

from prymatex import resources
from prymatex.utils.importlib import import_from_directory
from prymatex.utils import plist
from prymatex.utils import six

# TODO: por ahora este nombre esta bien, pero algo mas orientado a Prymatex server taria bueno
class ServerManager(QtCore.QObject, PMXBaseComponent):
    def __init__(self, application):
        QtCore.QObject.__init__(self, application)
        PMXBaseComponent.__init__(self)

        self.dialogs = {}
        self.instances = {}

        #Create socket
        self.socket = self.application.zmqSocket(zmq.REP, "Dialog", addressType='ipc')
        self.socket.readyRead.connect(self.socketReadyRead)
    
    @QtCore.Slot()
    def socketReadyRead(self):
        command = self.socket.recv_json()
        name = command.get("name")
        kwargs = command.get("kwargs", {})

        #TODO: Filtro todo lo que sea None asumo que las signaturas de los metodos ponene los valores por defecto
        # esto tendria que ser controlado de una mejor forma
        kwargs = dict([key_value for key_value in iter(kwargs.items()) if key_value[1] != None])
        
        self.logger.debug("Dialog Recv --> Method: %s, Arguments: %s" % (name, kwargs))
        method = getattr(self, name)
        try:
            method(**kwargs)
        except Exception as reason:
            self.sendResult({"error": {"code": -1, "message": six.text_type(reason)}})
            raise reason

    def loadDialogClass(self, moduleName, directory):
        # module = import_from_directory(directory, moduleName) if directory is not None else import_module(moduleName)
        module = import_from_directory(directory, moduleName)
        dialogClass = getattr(module, 'dialogClass')
        self.application.populateComponentClass(dialogClass)
        return dialogClass
        
    def createDialogInstance(self, dialogClass, mainWindow, async = False):
        instance = self.application.createComponentInstance(dialogClass, mainWindow)
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
            value = plist.writePlistToString(value)
        #Si tengo error retorno en lugar de result un error con { "code": <numero>, "message": "Cadena de error"}  
        #Ensure Unicode encode
        result = str(value).encode("utf-8")
        self.logger.debug("Dialog Send --> Result %s: %s" % (type(result), result))
        self.socket.send(result)
        
    def async_window(self, **kwargs):
        directory = os.path.dirname(kwargs["guiPath"])
        name = os.path.basename(kwargs["guiPath"])
        dialogClass = self.loadDialogClass(name, directory)
        instance, instanceId = self.createDialogInstance(dialogClass, self.application.mainWindow, async = True)
        if "parameters" in kwargs and kwargs["parameters"]:
            instance.setParameters(plist.readPlistFromString(kwargs["parameters"]))
        instance.show()
        self.sendResult(instanceId)
    
    def update_window(self, **kwargs):
        parameters = plist.readPlistFromString(kwargs["parameters"])
        instance = self.dialogInstance(int(kwargs["token"]))
        instance.setParameters(parameters)
        self.sendResult()

    def close_window(self, **kwargs):
        instance = self.dialogInstance(int(kwargs["token"]))
        instance.close()
        self.sendResult()

    def wait_for_input(self, **kwargs):
        instance = self.dialogInstance(int(kwargs["token"]))
        def sendInputResult(result):
            if result is not None:
                self.sendResult(result)
            else:
                self.sendResult({}) 
        instance.waitForInput(sendInputResult)

    def modal_window(self, **kwargs):
        parameters = plist.readPlistFromString(kwargs["parameters"])
        directory = os.path.dirname(kwargs["guiPath"])
        name = os.path.basename(kwargs["guiPath"])
        dialogClass = self.loadDialogClass(name, directory)
        instance = self.createDialogInstance(dialogClass, self.application.mainWindow)
        instance.setParameters(parameters)
        value = instance.execModal()
        self.sendResult({"result": value})

    def tooltip(self, message = "", format = "text", transparent = False):
        if message:
            self.application.currentEditor().showMessage(message)
        self.sendResult()
    
    def menu(self, **kwargs):
        parameters = plist.readPlistFromString(kwargs["parameters"])
        def sendSelectedIndex(index):
            if index != -1:
                self.sendResult({"selectedIndex": index})
            else:
                self.sendResult({})
            
        if "menuItems" in parameters:
            self.application.currentEditor().showFlatPopupMenu(parameters["menuItems"], sendSelectedIndex)

    def popup(self, **kwargs):
        suggestions = plist.readPlistFromString(kwargs["suggestions"])
        if kwargs.get("returnChoice", False):
            def sendSelectedSuggestion(suggestion):
                if suggestion is not None:
                    self.sendResult(suggestion)
                else:
                    self.sendResult({})
            self.application.currentEditor().showCompleter( suggestions = suggestions["suggestions"], 
                                                        alreadyTyped = kwargs.get("alreadyTyped"), 
                                                        caseInsensitive = kwargs.get("caseInsensitive", True),
                                                        callback = sendSelectedSuggestion)
        else:
            self.application.currentEditor().showCompleter( suggestions = suggestions["suggestions"], 
                                                        alreadyTyped = kwargs.get("alreadyTyped"), 
                                                        caseInsensitive = kwargs.get("caseInsensitive", True))
            self.sendResult()
        
    def defaults(self, **kwargs):
        return True
    
    def images(self, parameters = ""):
        data = plist.readPlistFromString(parameters)
        for name, path in data["register"].items():
            resources.registerImagePath(name, path)
        self.sendResult()
    
    def alert(self, **kwargs):
        self.sendResult()
    
    def mate(self, **kwargs):
        if "paths" in kwargs:
            for path in kwargs["paths"]:
                self.application.openFile(path)
        self.sendResult()
    
    def open(self, **kwargs):
        self.application.handleUrlCommand(kwargs["url"])
        self.sendResult()

    def completer(self, **kwargs):
        self.application.currentEditor().runCompleter()
        self.sendResult()
        
    def terminal(self, **kwargs):
        for command in kwargs["commands"]:
            self.application.mainWindow.terminalDock.runCommand(command)
        self.sendResult()

    def debug(self, **kwargs):
        print(kwargs)
        self.sendResult()
