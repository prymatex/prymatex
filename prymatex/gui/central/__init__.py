#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from prymatex.core import exceptions

class PMXBaseTab(object):
    #tabStatusChanged
    
    creation_counter = 0
    def __init__(self, fileInfo = None):
        self.fileInfo = fileInfo

    def setFileInfo(self, fileInfo):
        self.fileInfo = fileInfo
        self.emit(QtCore.SIGNAL("tabStatusChanged()"))
        
    def getTabIcon(self):
        return QtGui.QIcon()
    
    def getTabTitle(self):
        if self.fileInfo is not None:
            return self.fileInfo.fileName()
        elif not hasattr(self, "creation_counter"):
            self.creation_counter = PMXBaseTab.creation_counter
            PMXBaseTab.creation_counter += 1
        return "untitled %d" % self.creation_counter
    
    def isNew(self):
        return self.fileInfo is not None
        
    def isEmpty(self):
        return True
        
    def isModified(self):
        return False
    
    def close(self):
        while self.isModified():
            response = QtGui.QMessageBox.question(self, "Save", 
                unicode("Save %s" % self.getTabTitle()), 
                buttons = QtGui.QMessageBox.Ok | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel, 
                defaultButton = QMessageBox.Ok)
            if response == QtGui.QMessageBox.Ok:
                self.save()
            elif response == QtGui.QMessageBox.No:
                break
            elif response == QtGui.QMessageBox.Cancel:
                raise exceptions.UserCancelException()
    
    def save(self, saveAs = False):
        pass
    
    def zoomIn(self):
        pass

    def zoomOut(self):
        pass
    
    @classmethod
    def newInstance(cls, fileInfo = None, parent = None):
        return cls(fileInfo, parent)