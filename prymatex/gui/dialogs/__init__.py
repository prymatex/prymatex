#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from PyQt4 import QtGui

def getOpenFiles(directory):
    return QtGui.QFileDialog.getOpenFileNames(None, "Open Files", directory)

def getSaveFile(directory, name = "", title = "Save file", filters = []):
    filePath = os.path.join(directory, name) 
    
    filters = ";;".join(filters)
    name = QtGui.QFileDialog.getSaveFileName(None, title, filePath, filters)
    if name:
        return name
            
def confirmationDelete(parent = None):
    ok = QtGui.QMessageBox.question(parent, "Deletion confirmation", "<p>Are you sure you want to delete</p><p>%s</p>" % path, QtGui.QMessageBox.Ok | QtGui.QMessageBox.No)
        
def getFileName(extensions = [], directory = None, parent = None):
    name, ok = QtGui.QInputDialog.getText(parent, "New file name", "<p>Please enter the new file name in</p><p>%s</p>" % directory)
    if ok:
        return name

def getDirectoryName(directory = None, parent = None):
    name, ok = QtGui.QInputDialog.getText(parent, "New directoy name", "<p>Please enter the new directoy name in</p><p>%s</p>" % directory)
    if ok:
        return name