#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Command's module"""

import os
import sys
import functools

from prymatex.utils import programs

from .base import PMXBundleItem
from ..base import PMXRunningContext
from ..regexp import compileRegexp

# New commands
#input [ selection ]
#inputFormat [ text ]
#outputCaret [ afterOutput ]
#outputFormat [ html ]
#outputLocation [ newWindow ]
#requiredCommands [ 
#    {'command': git,
#     'locations': [ "/usr/local/git/bin/git", "/opt/local/bin/git", "/usr/local/bin/git" ] },
#     'variable': TM_GIT
#]

#namespace pre_exec { enum type { nop = 0, save_document, save_project }; }
#namespace input { enum type { selection = 0, entire_document, scope, line, word, character, nothing }; }
#namespace input_format { enum type { text = 0, xml }; }
#namespace output { enum type { replace_input = 0, replace_document, at_caret, after_input, new_window, tool_tip, discard, replace_selection }; }
#namespace output_format { enum type { text = 0, snippet, html, completion_list, snippet_no_auto_indent }; }
#namespace output_caret { enum type { after_output = 0, select_output, interpolate_by_char, interpolate_by_line, heuristic }; }

class PMXCommand(PMXBundleItem):
    KEYS = (    
        'input', 'fallbackInput', 'standardInput', 'inputFormat',               #Input
        #input [ "selection", "document", "scope", "line", "word", "character", "none" ]
        #inputFormat [ "text", "xml" ]
        'output', 'standardOutput', 'outputFormat', 'outputLocation',           #Output
        #outputLocation [ "replaceInput", "replaceDocument", "atCaret", "afterInput", "newWindow", "toolTip", "discard", "replaceSelection" ]
        #outputFormat [ "text", "snippet", "html", "completionList" ]
        'command', 'winCommand', 'linuxCommand',                                #System based Command
        'outputCaret',
        #[ "afterOutput", "selectOutput", "interpolateByChar", "interpolateByLine", "heuristic" ] },
        'beforeRunningCommand',                                                 #Antes de correr el command
        #[ "nop", "saveActiveFile", "saveModifiedFiles" ]
        'version',                                                              #Command version
        'requiredCommands',
        'require',
        'capturePattern', 'fileCaptureRegister',
        'columnCaptureRegister', 'disableOutputAutoIndent',
        'lineCaptureRegister', 'dontFollowNewOutput',
        'autoScrollOutput', 'captureFormatString', 'beforeRunningScript' )
    TYPE = 'command'
    FOLDER = 'Commands'
    EXTENSION = 'tmCommand'
    PATTERNS = ( '*.tmCommand', '*.plist' )
    # ------ Default Command content on create action
    DEFAULTS = {
        'name': 'untitled',
        'beforeRunningCommand': 'nop',
        'command': '''# just to remind you of some useful environment variables
# see Help / Environment Variables for the full list
echo File: "$TM_FILEPATH"
echo Word: "$TM_CURRENT_WORD"
echo Selection: "$TM_SELECTED_TEXT"''',
        'input': 'selection',
        'inputFormat': 'text',
        'fallbackInput': 'document',
        'output': 'replaceSelectedText',
        'outputFormat': 'text',
        'outputCaret': 'afterOutput'
    }
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
    
    # ---------------- Load, update, dump
    def __load_update(self, dataHash, initialize):
        for key in PMXCommand.KEYS:
            if key in dataHash or initialize:
                value = dataHash.get(key, None)
                if value is not None:
                    if key == 'capturePattern':
                        value = compileRegexp(value)
                setattr(self, key, value)
    
    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        self.__load_update(dataHash, True)
        # Remove cached values
        if hasattr(self, '_variables'):
            delattr(self, '_variables')
    
    def update(self, dataHash):
        PMXBundleItem.update(self, dataHash)
        self.__load_update(dataHash, False)
    
    def dump(self):
        dataHash = PMXBundleItem.dump(self)
        for key in PMXCommand.KEYS:
            value = getattr(self, key)
            if value != None:
                if key in ['capturePattern']:
                    value = str(value)
                dataHash[key] = value
        return dataHash
    
    # ---------------- Variables
    @property
    def variables(self):
        if not hasattr(self, '_variables'):
            self._variables = {}
            for program in self.requiredCommands or []:
                if not programs.is_program_installed(program["command"]):
                    # Search in locations
                    for location in program["locations"]:
                        if os.path.exists(location):
                            self._variables[program["variable"]] = location
                            break
        return self._variables
    
    # ---------------- Environment Variables
    def environmentVariables(self):
        environment = PMXBundleItem.environmentVariables(self)
        environment.update(self.variables)
        return environment
    
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
        if self.winCommand is not None and sys.platform.count("win"):
            return self.winCommand
        elif self.linuxCommand is not None:
            return self.linuxCommand
        else:
            return self.command
    
    def getOutputHandler(self, code):
        if self.output != 'showAsHTML' and code in self.EXIT_CODES:
            return self.EXIT_CODES[code]
        elif code != 0:
            return "error"
        else:
            return self.output or self.outputLocation
    
    def beforeExecute(self, processor):
        beforeMethod = None
        if self.beforeRunningCommand is not None:
            beforeMethod = getattr(processor, self.beforeRunningCommand)
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
        if context.inputType != None and outputHandler in [ "insertText", "insertAsSnippet", "replaceSelectedText", "replaceInput" ]:
            deleteMethod = getattr(processor, 'delete' + context.inputType.title(), None)
            if deleteMethod != None:
                deleteMethod()

        handlerFunction = getattr(processor, outputHandler, None)
        if handlerFunction is not None:
            handlerFunction(context, self.outputFormat)
        # TODO: Ver que pasa con el outputCaret
        # Delete temp file
        if outputHandler != "error":
            context.removeTempFile()
        processor.endCommand(self)

class PMXDragCommand(PMXCommand):
    KEYS = ( 'draggedFileExtensions', )
    TYPE = 'dragcommand'
    FOLDER = 'DragCommands'
    FILES = ( '*.tmCommand', '*.plist' )
    DEFAULTS = {
        'name': 'untitled',
        'draggedFileExtensions': ['png', 'jpg'],
        'command': '''echo "$TM_DROPPED_FILE"'''
    }

    # ---------------- Load, update, dump
    def __load_update(self, dataHash, initialize):
        for key in PMXDragCommand.KEYS:
            if key in dataHash or initialize:
                setattr(self, key, dataHash.get(key, None))
    
    def load(self, dataHash):
        PMXCommand.load(self, dataHash)
        self.__load_update(dataHash, True)
    
    def update(self, dataHash):
        PMXCommand.update(self, dataHash)
        self.__load_update(dataHash, False)

    def dump(self):
        dataHash = super(PMXDragCommand, self).dump()
        for key in PMXDragCommand.KEYS:
            value = getattr(self, key)
            dataHash[key] = value
        return dataHash
