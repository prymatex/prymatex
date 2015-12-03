#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import pprint

from prymatex.support import scripts

TEMPLATE = """Description: {description}
Asynchronous: {asynchronous}
Command: {command}
Working Directory: {workingDirectory}
Variables: {variables}
Environment: {environment}
Script Path: {scriptFilePath}
Script Environment: {scriptFileEnvironment}
Input Type: {inputType}
Input Value: {inputValue}
OutputType: {outputType}
OutputValue: {outputValue}
ErrorValue: {errorValue}
"""

class RunningContext(object):
    command = None
    environment = None
    variables = None
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
        self.command = attrs.pop("command")
        
        # Environment
        self.environment = attrs.pop("environment", {})
        
        # Variables
        self.variables = attrs.pop("variables", [])

        # Asynchronous ?
        self.asynchronous = attrs.pop("asynchronous", False)
        
        # Has Working Directory ?
        self.workingDirectory = attrs.pop("workingDirectory", None)
        
        # Has Input ?
        self.inputValue = attrs.pop("inputValue", None)
        
        # Has Callback ?
        self.callback = attrs.pop("callback", None)
        
        self.scriptFilePath, self.scriptFileEnvironment = scripts.buildShellScriptContext(
            self.command, self.environment, self.variables)

        for key, value in attrs.items():
            setattr(self, key, value)
            
    def __delete__(self):
        self.removeScriptFile()

    def __str__(self):
        return TEMPLATE.format(
            description=self.description(),
            asynchronous=self.asynchronous,
            command=self.command,
            workingDirectory=self.workingDirectory,
            variables=pprint.pformat(self.variables),
            environment=pprint.pformat(self.environment),
            inputType=self.inputType,
            inputValue=self.inputValue,
            scriptFilePath=self.scriptFilePath,
            scriptFileEnvironment=pprint.pformat(self.scriptFileEnvironment),
            outputType=self.outputType,
            outputValue=self.outputValue,
            errorValue=self.errorValue
        )

    __unicode__ = __str__
    
    def isBundleItem(self, bundleItem):
        return self.bundleItem == bundleItem

    def description(self):
        return hasattr(self, "bundleItem") and self.bundleItem.name or "%s..." % self.command[:10]
        
    def removeScriptFile(self):
        if os.path.exists(self.scriptFilePath):
            scripts.deleteFile(self.scriptFilePath)
