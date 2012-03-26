#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Command's module"""

import os
import functools
from collections import namedtuple

from prymatex.support.bundle import PMXBundleItem
from prymatex.support.utils import compileRegexp, prepareShellScript

#TODO: Hacer un PMXRunningContext para todo lo que requiera de procesos template, commands, etc
class PMXRunningContext(object):
    def __init__(self, command):
        self.command = command
        self.inputType, self.inputValue = "", ""
        self.shellCommand, self.environment = "", {}
        self.asynchronous = False
        self.outputValue = self.outputType = None
        
class PMXCommand(PMXBundleItem):
    KEYS = [    'input', 'fallbackInput', 'standardInput', 'output', 'standardOutput',  #I/O
                'command', 'winCommand', 'linuxCommand',                                #System based Command
                'inputFormat',                                                          #Formato requerido en la entrada
                'beforeRunningCommand',                                                 #Antes de correr el command
                'capturePattern', 'fileCaptureRegister',
                'columnCaptureRegister', 'disableOutputAutoIndent',
                'lineCaptureRegister', 'dontFollowNewOutput',
                'autoScrollOutput', 'captureFormatString', 'beforeRunningScript' ]
    TYPE = 'command'
    FOLDER = 'Commands'
    EXTENSION = 'tmCommand'
    PATTERNS = ['*.tmCommand', '*.plist']
    exit_codes = {
                  200: 'discard',
                  201: 'replaceSelectedText',
                  202: 'replaceDocument',
                  203: 'insertText',
                  204: 'insertAsSnippet',
                  205: 'showAsHTML',
                  206: 'showAsTooltip',
                  207: 'createNewDocument'
                  }
    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        for key in PMXCommand.KEYS:
            value = dataHash.get(key, None)
            if value != None and key in [    'capturePattern' ]:
                value = compileRegexp( value )
            setattr(self, key, value)
    
    @property
    def hash(self):
        dataHash = super(PMXCommand, self).hash
        for key in PMXCommand.KEYS:
            value = getattr(self, key)
            if value != None:
                if key in ['capturePattern']:
                    value = unicode(value)
                dataHash[key] = value
        return dataHash

    def getInputText(self, processor):
        def getInputTypeAndValue(input, format):
            if input is None or input == "none": return None, None
            return input, getattr(processor, input)(format)
        input, value = getInputTypeAndValue(self.input, self.inputFormat)
        if value == None and self.fallbackInput != None:
            input, value = getInputTypeAndValue(self.fallbackInput, self.inputFormat)
        if value == None and self.standardInput != None:
            input, value = getInputTypeAndValue(self.standardInput, self.inputFormat)

        if input == 'selection' and value == None:
            value = processor.document(self.inputFormat)
            input = "document"
        elif value == None:
            input = None
        return input, value
    
    def systemCommand(self):
        if self.winCommand != None and 'Window' in os.environ['OS']:
            return self.winCommand
        elif self.linuxCommand != None:
            return self.linuxCommand
        else:
            return self.command
    
    def getOutputHandler(self, code):
        if self.output != 'showAsHTML' and code in self.exit_codes:
            return self.exit_codes[code]
        elif code != 0:
            return "error"
        else:
            return self.output
    
    def beforeExecute(self, processor):
        if not hasattr(self, 'beforeRunningCommand') or self.beforeRunningCommand == None: return True
        return getattr(processor, self.beforeRunningCommand)()

    def execute(self, processor):
        #if not self.beforeExecute(processor): return
        
        context = PMXRunningContext(self)
        
        context.asynchronous = processor.asynchronous
        context.inputType, context.inputValue = self.getInputText(processor)
        context.shellCommand, context.environment = prepareShellScript(self.systemCommand(), processor.environment(self))

        self.manager.runProcess(context, functools.partial(self.afterExecute, processor))
    
    def afterExecute(self, processor, context):
        outputHandler = self.getOutputHandler(context.outputType)
        # Remove old
        if context.inputType != None and outputHandler in [ "insertText", "insertAsSnippet", "replaceSelectedText" ]:
            deleteMethod = getattr(processor, 'delete' + context.inputType.title(), None)
            if deleteMethod != None:
                deleteMethod()

        getattr(processor, outputHandler, None)(context)

class PMXDragCommand(PMXCommand):
    KEYS = [    'draggedFileExtensions' ]
    TYPE = 'dragcommand'
    FOLDER = 'DragCommands'
    FILES = ['*.tmCommand', '*.plist']

    def load(self, dataHash):
        PMXCommand.load(self, dataHash)
        for key in PMXDragCommand.KEYS:
            value = dataHash.get(key, None)
            setattr(self, key, value)
    
    @property
    def hash(self):
        dataHash = super(PMXDragCommand, self).hash
        for key in PMXDragCommand.KEYS:
            value = getattr(self, key)
            dataHash[key] = value
        return dataHash
        