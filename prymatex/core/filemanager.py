#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, codecs, shutil
from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.core.settings import pmxConfigPorperty
from prymatex.core.exceptions import APIUsageError, PrymatexIOException, PrymatexFileExistsException

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
    
    def createDirectory(self, directory):
        """
        Create a new directory.
        """
        if os.path.exists(directory):
            raise PrymatexIOException("The directory already exist") 
        os.mkdir(directory)
    
    def createDirectories(directory):
        """Create a group of directory, one inside the other."""
        if os.path.exists(directory):
            raise PrymatexIOException("The folder already exist")
        os.makedirs(directory)
    
    def createFile(self, file):
        """Create a new file."""
        if os.path.exists(file):
            raise PrymatexIOException("The file already exist") 
        open(path, 'w').close()
    
    def renameFile(old, new):
        """Rename a file, changing its name from 'old' to 'new'."""
        if os.path.isfile(old):
            if os.path.exists(new):
                raise NinjaFileExistsException(new)
            os.rename(old, new)
            return new
        return ''
    
    def deletePath(self, path):
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
