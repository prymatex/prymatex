#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Command's module    
'''
import os
from collections import namedtuple

from prymatex.support.bundle import PMXBundleItem
from prymatex.support.utils import compileRegexp, prepareShellScript

#TODO: Hacer un PMXRunningContext para todo lo que requiera de procesos template, commands, etc
class PMXCommandContext(object):
    def __init__(self, command, environment, inputType, inputValue, outputType = None, outputValue = None):
        self.command = command
        self.environment = environment
        self.inputType = inputType
        self.inputValue = inputValue
        self.outputType = outputType
        self.outputValue = outputValue

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
        inputType, inputValue = self.getInputText(processor)
        shellCommand, environment = prepareShellScript(self.systemCommand(), processor.environment(self))
        
        context = PMXCommandContext(self, environment, inputType, inputValue)
        
        processor.runCommand(context, shellCommand, self.afterExecute)
    
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
        