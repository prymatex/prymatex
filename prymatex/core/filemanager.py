#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, codecs, shutil
from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.core.settings import pmxConfigPorperty
from prymatex.core.exceptions import APIUsageError, PrymatexIOException

class PMXFileManager(PMXObject):
    """
    A File Manager
    """
    #=========================================================
    # Signals
    #=========================================================
    fileOpened = QtCore.pyqtSignal()
    
    #=========================================================
    # Settings
    #=========================================================
    SETTINGS_GROUP = 'FileManager'

    fileHistory = pmxConfigPorperty(default=[])
    fileHistoryLength = pmxConfigPorperty(default=10)
    
    def __init__(self, parent):
        super(PMXFileManager, self).__init__(parent)

        self.iconProvider = QtGui.QFileIconProvider()
        self._default_directory = QtCore.QDir(self.application.settings.USER_HOME_PATH)
        self.configure()

    def _add_file_history(self, fileInfo):
        path = fileInfo.absoluteFilePath()
        if path in self.fileHistory:
            self.fileHistory.remove(path)
        self.fileHistory.insert(0, path)
        if len(self.fileHistory) > self.fileHistoryLength:
            self.fileHistory = self.fileHistory[0:self.fileHistoryLength]
        self.settings.setValue("fileHistory", self.fileHistory)
    
    def clearFileHistory(self):
        self.fileHistory = []
        self.settings.setValue("fileHistory", self.fileHistory)
    
    def createDirectory(self, base, name = None, parent = None):
        """Create a new directory."""
        if name is None:
            name, ok = QtGui.QInputDialog.getText(parent, "New directoy name", "<p>Please enter the new directoy name in</p><p>%s</p>" % base)
            if not ok:
                return None
        path = os.path.join(base, name)
        if os.path.exists(path):
            raise PrymatexIOException("The directory already exist") 
        os.mkdir(path)
        return QtCore.QFileInfo(path)
    
    def createFile(self, base, name = None, parent = None):
        """Create a new file."""
        if name is None:
            name, ok = QtGui.QInputDialog.getText(parent, "New file name", "<p>Please enter the new file name in</p><p>%s</p>" % base)
            if not ok:
                return None
        path = os.path.join(base, name)
        if os.path.exists(path):
            raise PrymatexIOException("The file already exist") 
        open(path, 'w').close()
        return QtCore.QFileInfo(path)
    
    def deletePath(self, path, parent = None):
        ok = QtGui.QMessageBox.question(parent, "Deletion confirmation", "<p>Are you sure you want to delete</p><p>%s</p>" % path, 
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.No)
        if ok == QtGui.QMessageBox.Ok: 
            if os.path.isfile(path):
                # Mandar señal para cerrar editores
                os.unlink(path)
            else:
                shutil.rmtree(path)
    
    def openFile(self, fileInfo):
        """Open and read a file, return the content."""
        if not fileInfo.exists():
            raise PrymatexIOException("The file does not exist")
        if not fileInfo.isFile():
            raise PrymatexIOException("%s is not a file" % fileInfo)
        f = QtCore.QFile(fileInfo.absoluteFilePath())
        if not f.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
            raise PrymatexIOException("%s" % f.errorString())
        stream = QtCore.QTextStream(f)
        content = stream.readAll()
        f.close()
        #Update file history
        self._default_directory = fileInfo.dir()
        self._add_file_history(fileInfo)
        return content
    
    def saveFile(self, fileInfo, content):
        """
        Function that actually save the content of a file.
        """
        try:
            f = QtCore.QFile(fileInfo.absoluteFilePath())
            if not f.open(QtCore.QIODevice.WriteOnly | QtCore.QIODevice.Truncate):
                raise PrymatexIOException(f.errorString())
            stream = QtCore.QTextStream(f)
            encoded_stream = stream.codec().fromUnicode(content)
            f.write(encoded_stream)
            f.flush()
            f.close()
        except:
            raise
    
    def getDirectory(self, fileInfo = None):
        """
        Obtiene un directorio para el fileInfo
        """
        if fileInfo is None:
            #if fileInfo is None return the las directory or the home directory
            return self._default_directory
        return fileInfo.dir()
        
    def getOpenFiles(self, fileInfo = None):
        directory = self.getDirectory(fileInfo)
        names = QtGui.QFileDialog.getOpenFileNames(None, "Open Files", directory.absolutePath())
        return map(lambda name: QtCore.QFileInfo(name), names)
    
    def getSaveFile(self, fileInfo = None, name = "", title = "Save file", filters = []):
        directory = self.getDirectory(fileInfo)
        filePath = directory.absoluteFilePath(name) if name else directory.absolutePath()

        filters = ";;".join(filters)
        name = QtGui.QFileDialog.getSaveFileName(None, title, filePath, filters)
        if name:
            return QtCore.QFileInfo(name)
    
    def getFileIcon(self, fileInfo):
        if fileInfo.exists():
            return self.iconProvider.icon(fileInfo)
        return self.iconProvider.icon(QtGui.QFileIconProvider.File)
    
    def getFileType(self, fileInfo):
        return self.iconProvider.type(fileInfo)
    