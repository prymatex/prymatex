#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import sys
import tempfile
import socket
import json

from prymatex import resources
from prymatex.core import PrymatexComponent
from prymatex.qt import QtCore, QtGui, QtNetwork

from prymatex.utils.importlib import import_from_directories
from prymatex.utils import plist
from prymatex.utils import six
from prymatex.utils import encoding

# TODO: por ahora este nombre esta bien, pero algo mas orientado a Prymatex server taria bueno
class ServerManager(PrymatexComponent, QtCore.QObject):
    def __init__(self, **kwargs):
        super(ServerManager, self).__init__(**kwargs)
        self.dialogs = {}
        self.instances = {}
        self.address = tempfile.mktemp(prefix="pmx")
        self.server = QtNetwork.QLocalServer(self)
        self.server.listen(self.address)
        self.server.newConnection.connect(self.on_server_newConnection)

    def environmentVariables(self):
        """Return a dictionary with the defined variables of this component."""
        env = {}
        if self.address is not None:
            env["PMX_DIALOG_ADDRESS"] = self.address
        return env    

    def on_server_newConnection(self):
        connection = self.server.nextPendingConnection()
        connection.readyRead.connect(lambda con = connection: self.socketReadyRead(con))

    def socketReadyRead(self, connection):
        command = json.loads(encoding.from_fs(connection.readAll().data()))
        name = command.get("name")
        args = command.get("args", [])
        kwargs = command.get("kwargs", {})
        
        args.insert(0, connection)
        #TODO: Filtro todo lo que sea None asumo que las signaturas de los metodos ponene los valores por defecto
        # esto tendria que ser controlado de una mejor forma
        kwargs = dict([key_value for key_value in iter(kwargs.items()) if key_value[1] != None])
        
        self.logger().debug("Dialog Recv --> Method: %s, Arguments: %s" % (name, kwargs))
        method = getattr(self, name)
        try:
            method(*args, **kwargs)
        except Exception as reason:
            self.sendResult({"error": {"code": -1, "message": six.text_type(reason)}})
            raise reason

    def loadDialogClass(self, moduleName, directory):
        module = import_from_directories([ directory ], moduleName)
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
        
    def sendResult(self, connection, value=None):
        if value is None:
            value = ""
        if isinstance(value, int):
            value = "%d" % value
        if isinstance(value, dict):
            value = plist.writePlistToString(value)
        #Si tengo error retorno en lugar de result un error con { "code": <numero>, "message": "Cadena de error"}  
        result = encoding.to_fs(value)
        self.logger().debug("Dialog Send --> Result %s: %s" % (type(result), result))
        connection.send(result)
        
    def async_window(self, connection, **kwargs):
        directory = os.path.dirname(kwargs["guiPath"])
        name = os.path.basename(kwargs["guiPath"])
        dialogClass = self.loadDialogClass(name, directory)
        instance, instanceId = self.createDialogInstance(dialogClass, self.application.mainWindow, async = True)
        if "parameters" in kwargs and kwargs["parameters"]:
            instance.setParameters(plist.readPlistFromString(kwargs["parameters"]))
        instance.show()
        self.sendResult(connection, instanceId)
    
    def update_window(self, connection, **kwargs):
        parameters = plist.readPlistFromString(kwargs["parameters"])
        instance = self.dialogInstance(int(kwargs["token"]))
        instance.setParameters(parameters)
        self.sendResult(connection)

    def close_window(self, connection, **kwargs):
        instance = self.dialogInstance(int(kwargs["token"]))
        instance.close()
        self.sendResult(connection)

    def wait_for_input(self, connection, **kwargs):
        instance = self.dialogInstance(int(kwargs["token"]))
        def sendInputResult(connection):
            def _send(result):
                if result is not None:
                    self.sendResult(connection, result)
                else:
                    self.sendResult(connection, {}) 
            return _send
        instance.waitForInput(sendInputResult(connection))

    def modal_window(self, connection, **kwargs):
        parameters = plist.readPlistFromString(kwargs["parameters"])
        directory = os.path.dirname(kwargs["guiPath"])
        name = os.path.basename(kwargs["guiPath"])
        dialogClass = self.loadDialogClass(name, directory)
        instance = self.createDialogInstance(dialogClass, self.application.mainWindow)
        instance.setParameters(parameters)
        value = instance.execModal()
        self.sendResult(connection, {"result": value})

    def tooltip(self, connection, message = "", format = "text", transparent = False):
        if message:
            self.application.currentEditor().showMessage(message)
        self.sendResult(connection)
    
    def menu(self, connection, **kwargs):
        parameters = plist.readPlistFromString(kwargs["parameters"])
        def sendSelectedIndex(connection):
            def _send(index):
                if index != -1:
                    self.sendResult(connection, {"selectedIndex": index})
                else:
                    self.sendResult(connection, {})
            return _send

        if "menuItems" in parameters:
            self.application.currentEditor().showFlatPopupMenu(parameters["menuItems"], sendSelectedIndex(connection))

    def popup(self, connection, **kwargs):
        suggestions = plist.readPlistFromString(kwargs["suggestions"])
        if kwargs.get("returnChoice", False):
            def sendSelectedSuggestion(connection):
                def _send(suggestion):
                    if suggestion is not None:
                        self.sendResult(connection, suggestion)
                    else:
                        self.sendResult(connection, {})
                return _send
            self.application.currentEditor().runCompleter( suggestions = suggestions["suggestions"], 
                                                        already_typed = kwargs.get("alreadyTyped"), 
                                                        case_insensitive = kwargs.get("caseInsensitive", True),
                                                        callback = sendSelectedSuggestion(connection))
        else:
            self.application.currentEditor().runCompleter( suggestions = suggestions["suggestions"], 
                                                        already_typed = kwargs.get("alreadyTyped"), 
                                                        case_insensitive = kwargs.get("caseInsensitive", True))
            self.sendResult(connection)
    
    def defaults(self, connection, **kwargs):
        return True
    
    def images(self, connection, parameters = ""):
        data = plist.readPlistFromString(parameters)
        for name, path in data["register"].items():
            resources.set_resource("External", name, path)
        self.sendResult(connection)
    
    def alert(self, connection, **kwargs):
        self.sendResult(connection)
    
    def mate(self, connection, **kwargs):
        if "paths" in kwargs:
            for path in kwargs["paths"]:
                self.application.openFile(path)
        self.sendResult(connection)
    
    def open(self, connection, **kwargs):
        self.application.openUrl(kwargs["url"])
        self.sendResult(connection)
    
    def terminal(self, connection, **kwargs):
        for command in kwargs["commands"]:
            self.application.mainWindow.terminalDock.runCommand(command)
        self.sendResult(connection)

    def debug(self, connection, **kwargs):
        print(kwargs)
        self.sendResult(connection)
