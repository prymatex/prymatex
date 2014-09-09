#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Command's module"""

import os
import sys
import functools

from prymatex.utils import programs

from .base import BundleItem
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

class Command(BundleItem):
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
    def __init__(self, *largs, **kwargs):
        super(Command, self).__init__(*largs, **kwargs)
        self._variables = None

    # ---------------- Load, update, dump
    def __load_update(self, dataHash, initialize):
        for key in Command.KEYS:
            if key in dataHash or initialize:
                value = dataHash.get(key, None)
                if value is not None:
                    if key == 'capturePattern':
                        value = compileRegexp(value)
                setattr(self, key, value)

    def load(self, dataHash):
        BundleItem.load(self, dataHash)
        self.__load_update(dataHash, True)
        # Remove cached values
        self._variables = None

    def update(self, dataHash):
        BundleItem.update(self, dataHash)
        self.__load_update(dataHash, False)

    def dump(self, allKeys = False):
        dataHash = BundleItem.dump(self, allKeys)
        for key in Command.KEYS:
            value = getattr(self, key, None)
            if allKeys or value is not None:
                if key == 'capturePattern' and value is not None:
                    value = value.pattern
                dataHash[key] = value
        return dataHash

    # ---------------- Variables
    def variables(self):
        if self._variables is None:
            self._variables = {}
            for r in self.require or []:
                bundle = self.manager.getBundle(r["uuid"])
                if bundle is not None:
                    self._variables.update(bundle.variables())
                    support = bundle.supportPath()
                    if support is not None:
                        self._variables["TM_%s_BUNDLE_SUPPORT" % r["name"].upper()] = support
            self._variables.update(self.bundle.variables())
            for program in self.requiredCommands or []:
                if not programs.is_program_installed(program["command"]):
                    # Search in locations
                    for location in program["locations"]:
                        if os.path.exists(location):
                            self._variables[program["variable"]] = location
                            break
            
        return self._variables.copy()

    # ---------------- Environment Variables
    def environmentVariables(self):
        env = BundleItem.environmentVariables(self)
        env.update(self.variables())
        return env

    def getInputText(self, processor):
        def getInputTypeAndValue(inputType, inputFormat, inputMode):
            if inputType in (None, False, "none"): return None, None
            return inputType, getattr(processor, inputType)(inputFormat = inputFormat, inputMode = inputMode)

        # -------- Try input
        inputType, inputValue = getInputTypeAndValue(self.input, self.inputFormat, "input")

        # -------- Try fallback
        if not inputValue:
            fallbackInput = self.fallbackInput or (self.input == 'selection' and 'document')
            inputType, inputValue = getInputTypeAndValue(fallbackInput, self.inputFormat, "fallback")

        # -------- Try standard
        if not inputValue:
            inputType, inputValue = getInputTypeAndValue(self.standardInput, self.inputFormat, "standard")
        
        print(inputValue)
        return inputType, inputValue

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
        # Has requirements
        # TODO: Avisar al processor porque no corremos
        if any([self.manager.getBundle(r["uuid"]) is None for r in self.require or []]):
            return False
        # Before running command
        if self.beforeRunningCommand is not None:
            return getattr(processor, self.beforeRunningCommand)()
        return True

    def execute(self, processor):
        self.executeCallback(processor, functools.partial(self.afterExecute, processor))

    def executeCallback(self, processor, callback):
        processor.beginExecution(self)
        if self.beforeExecute(processor):
            inputType, inputValue = self.getInputText(processor)
            self.manager.runSystemCommand(
                bundleItem = self,
                shellCommand = self.systemCommand(),
                environment = processor.environmentVariables(),
                shellVariables = processor.shellVariables(),
                asynchronous = processor.asynchronous,
                inputType = inputType,
                inputValue = inputValue,
                callback = callback
            )

    def afterExecute(self, processor, context):
        outputHandler = self.getOutputHandler(context.outputType)

        handlerFunction = getattr(processor, outputHandler, None)
        if handlerFunction is not None:
            handlerFunction(context, self.outputFormat)
        # TODO: Ver que pasa con el outputCaret
        # Delete temp file
        if outputHandler != "error":
            context.removeScriptFile()
        processor.endExecution(self)

class DragCommand(Command):
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
        for key in DragCommand.KEYS:
            if key in dataHash or initialize:
                setattr(self, key, dataHash.get(key, None))

    def load(self, dataHash):
        Command.load(self, dataHash)
        self.__load_update(dataHash, True)

    def update(self, dataHash):
        Command.update(self, dataHash)
        self.__load_update(dataHash, False)

    def dump(self, allKeys = False):
        dataHash = Command.dump(self, allKeys)
        for key in DragCommand.KEYS:
            value = getattr(self, key, None)
            if allKeys or value is not None:
                dataHash[key] = value
        return dataHash
