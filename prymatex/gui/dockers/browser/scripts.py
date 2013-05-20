#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore

#=======================================================================
# System process wrapper
# wrap a process for using in window context of javascript
#=======================================================================
class SystemWrapper(QtCore.QObject):
    def __init__(self, wrappedProcess):
        QtCore.QObject.__init__(self)
        self.wrappedProcess = wrappedProcess

    @QtCore.Slot(str)
    def write(self, data):
        self.wrappedProcess.stdin.write(data)

    @QtCore.Slot()
    def read(self):
        self.wrappedProcess.stdin.close()
        text = self.wrappedProcess.stdout.read()
        self.wrappedProcess.stdout.close()
        self.wrappedProcess.wait()
        return text

    @QtCore.Slot()
    def close(self):
        self.wrappedProcess.stdin.close()
        self.wrappedProcess.stdout.close()
        self.wrappedProcess.wait()

    def outputString(self):
        self.wrappedProcess.stdin.close()
        text = self.wrappedProcess.stdout.read()
        self.wrappedProcess.stdout.close()
        self.wrappedProcess.wait()
        return text
    outputString = QtCore.Property(str, outputString)

#=======================================================================
# Custom JavaScript for using with pages generated by prymatex
#=======================================================================
WINDOW_JAVASCRIPT = """
%s
TextMate.system = function(command, callback) {
    this._system(command);
    if (callback != null) {
        
    }
    return _systemWrapper;
}
"""
    
class TextMate(QtCore.QObject):
    @QtCore.Slot(str)
    def _system(self, command):
        self.parent().runCommand(command)
            
    def isBusy(self):
        return True
    isBusy = QtCore.Property("bool", isBusy)