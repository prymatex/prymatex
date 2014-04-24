#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from prymatex.support import scripts

class RunningContext(object):
    TEMPLATE = """Item Name: {itemName}
    Asynchronous: {asynchronous}
    Working Directory: {workingDirectory}
    Input:  Type {inputType}, Value {inputValue}
    Environment: {environment}
    OutputType: {outputType}
    OutputValue: {outputValue}
    ErrorValue: {errorValue}
    """
    shellCommand = None
    environment = None
    shellVariables = None
    asynchronous = False
    workingDirectory = None
    inputType = None
    inputValue = None
    outputType = None
    outputValue = None
    process = None
    errorValue = None
    callback = None
    
    def __init__(self, **attrs):
        
        # Command
        self.shellCommand = attrs.pop("shellCommand")
        
        # Environment
        self.environment = attrs.pop("environment", {})
        
        # Variables
        self.shellVariables = attrs.pop("shellVariables", [])

        # Asynchronous ?
        self.asynchronous = attrs.pop("asynchronous", False)
        
        # Has Working Directory ?
        self.workingDirectory = attrs.pop("workingDirectory", None)
        
        # Has Input ?
        self.inputValue = attrs.pop("inputValue", None)
        
        # Has Callback ?
        self.callback = attrs.pop("callback", None)
        
        self.scriptFilePath, self.scriptFileEnvironment = scripts.buildShellScriptContext(
            self.shellCommand, self.environment, self.shellVariables)

        for key, value in attrs.items():
            setattr(self, key, value)
            
    def __delete__(self):
        self.removeScriptFile()

    def __unicode__(self):
        return self.TEMPLATE.format(
            itemName = hasattr(self, "bundleItem") and \
                self.bundleItem.name or "None item",
            asynchronous = self.asynchronous,
            workingDirectory = self.workingDirectory,
            inputType = self.inputType,
            inputValue = self.inputValue,
            environment = self.environment,
            outputType = self.outputType,
            outputValue = self.outputValue,
            errorValue = self.errorValue
        )

    def __str__(self):
        return self.TEMPLATE.format(
            itemName = hasattr(self, "bundleItem") and \
                self.bundleItem.name or "None item",
            asynchronous = self.asynchronous,
            workingDirectory = self.workingDirectory,
            inputType = self.inputType,
            inputValue = self.inputValue,
            environment = self.environment,
            outputType = self.outputType,
            outputValue = self.outputValue,
            errorValue = self.errorValue
        )

    def isBundleItem(self, bundleItem):
        return self.bundleItem == bundleItem

    def description(self):
        return hasattr(self, "bundleItem") and self.bundleItem.name or "No Name"
        
    def removeScriptFile(self):
        if os.path.exists(self.scriptFilePath):
            scripts.deleteFile(self.scriptFilePath)
