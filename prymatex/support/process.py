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
    def __init__(self, **attrs):
        # Before run attr
        self.shellCommand, self.environment, self.tempFile = scripts.prepareShellScript(
            attrs.pop("shellCommand"), attrs.pop("environment", {}))
        
        self.asynchronous = attrs.pop("asynchronous", False)
        self.workingDirectory = attrs.pop("workingDirectory", None)
        self.inputValue = attrs.pop("inputValue", None)
        self.callback = attrs.pop("callback", None)
        
        # After run attrs
        self.process = self.errorValue = self.outputValue = self.outputType = None
        
        for key, value in attrs.items():
            setattr(self, key, value)
            
    def __delete__(self):
        self.removeTempFile()

    def __unicode__(self):
        return self.TEMPLATE.format(
            itemName = self.bundleItem.name,
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
            itemName = self.bundleItem.name,
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
        return self.bundleItem.name or "No Name"
        
    def removeTempFile(self):
        if os.path.exists(self.tempFile):
            scripts.deleteFile(self.tempFile)