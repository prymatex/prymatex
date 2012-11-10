#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Command's module"""

import os
import functools
from collections import namedtuple

from prymatex.support.bundle import PMXBundleItem, PMXRunningContext
from prymatex.support.utils import compileRegexp

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
    EXIT_CODES = {
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
        def getInputTypeAndValue(inputType, format):
            if inputType is None or inputType == "none": return None, None
            return inputType, getattr(processor, inputType)(format)
        inputType, value = getInputTypeAndValue(self.input, self.inputFormat)
        if value is None and self.fallbackInput is not None:
            inputType, value = getInputTypeAndValue(self.fallbackInput, self.inputFormat)
        if value is None and self.standardInput is not None:
            inputType, value = getInputTypeAndValue(self.standardInput, self.inputFormat)
        if inputType == 'selection' and value is None:
            value = processor.document(self.inputFormat)
            inputType = "document"
        elif value is None:
            inputType = None
        return inputType, value
    
    def systemCommand(self):
        if self.winCommand != None and 'Window' in os.environ['OS']:
            return self.winCommand
        elif self.linuxCommand != None:
            return self.linuxCommand
        else:
            return self.command
    
    def getOutputHandler(self, code):
        if self.output != 'showAsHTML' and code in self.EXIT_CODES:
            return self.EXIT_CODES[code]
        elif code != 0:
            return "error"
        else:
            return self.output
    
    def beforeExecute(self, processor):
        beforeMethod = None
        if self.beforeRunningCommand is not None:
            beforeMethod  = getattr(processor, self.beforeRunningCommand)
            return beforeMethod()
        return True

    def execute(self, processor):
        self.executeCallback(processor, functools.partial(self.afterExecute, processor))
        
    def executeCallback(self, processor, callback):
        processor.startCommand(self)
        if self.beforeExecute(processor):
            with PMXRunningContext(self, self.systemCommand(), processor.environmentVariables()) as context:
                context.asynchronous = processor.asynchronous
                context.inputType, context.inputValue = self.getInputText(processor)
                self.manager.runProcess(context, callback)
                
    def afterExecute(self, processor, context):
        outputHandler = self.getOutputHandler(context.outputType)
        # Remove old
        if context.inputType != None and outputHandler in [ "insertText", "insertAsSnippet", "replaceSelectedText" ]:
            deleteMethod = getattr(processor, 'delete' + context.inputType.title(), None)
            if deleteMethod != None:
                deleteMethod()

        handlerFunction = getattr(processor, outputHandler, None)
        if handlerFunction is not None:
            handlerFunction(context)
        
        #Delete temp file
        context.removeTempFile()
        processor.endCommand(self)

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
        