#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import codecs
import shutil
import mimetypes
from PyQt4 import QtCore, QtGui
from prymatex.core.settings import pmxConfigPorperty
from prymatex.core.exceptions import APIUsageError, PrymatexIOException, PrymatexFileExistsException
from functools import partial

class PMXFileManager(QtCore.QObject):
    """
    A File Manager
    """
    #=========================================================
    # Signals
    #=========================================================
    fileCreated = QtCore.pyqtSignal(str)
    fileDeleted = QtCore.pyqtSignal(str)
    fileChanged = QtCore.pyqtSignal(str)
    fileRenamed = QtCore.pyqtSignal(str, str)
    directoryCreated = QtCore.pyqtSignal(str)
    directoryDeleted = QtCore.pyqtSignal(str)
    directoryChanged = QtCore.pyqtSignal(str)
    directoryRenamed = QtCore.pyqtSignal(str, str)
    # Generic Signal 
    filesytemChange = QtCore.pyqtSignal(str, int)
    
    #=========================================================
    # Settings
    #=========================================================
    SETTINGS_GROUP = 'FileManager'

    fileHistory = pmxConfigPorperty(default = [])
    fileHistoryLength = pmxConfigPorperty(default = 10)
    lineEnding = pmxConfigPorperty(default = 'unix')
    encoding = pmxConfigPorperty(default = 'utf-8')

    #=========================================================
    # Constants
    #=========================================================
    CREATED = 1<<0
    DELETED = 1<<1
    RENAMED = 1<<2
    MOVED   = 1<<3
    CHANGED = 1<<4    

    def __init__(self, application):
        QtCore.QObject.__init__(self)
        
        self.last_directory = application.settings.USER_HOME_PATH
        self.fileWatcher = QtCore.QFileSystemWatcher()
        self.fileWatcher.fileChanged.connect(self.on_fileChanged)
        self.fileWatcher.directoryChanged.connect(self.on_directoryChanged)
        self.connectGenericSignal()

    @classmethod
    def contributeToSettings(cls):
        return [ ]
        
    def connectGenericSignal(self):
        UNARY_SINGAL_CONSTANT_MAP = (
            (self.fileCreated, PMXFileManager.CREATED ),
            (self.fileDeleted, PMXFileManager.DELETED ),
            (self.fileChanged, PMXFileManager.CHANGED ),
            (self.directoryCreated, PMXFileManager.CREATED ),
            (self.directoryDeleted, PMXFileManager.DELETED ),
            (self.directoryChanged, PMXFileManager.CHANGED ),
        )
        BINARY_SINGAL_CONSTANT_MAP = (
            (self.fileRenamed, PMXFileManager.RENAMED ),
            (self.directoryRenamed, PMXFileManager.RENAMED ),                       
        )
        for signal, associatedConstant in UNARY_SINGAL_CONSTANT_MAP:
            signal.connect(lambda path, constant = associatedConstant: self.filesytemChange.emit(path, constant))
        for signal, associatedConstant in BINARY_SINGAL_CONSTANT_MAP:
            signal.connect(lambda _x, path, constant = associatedConstant: self.filesytemChange.emit(path, constant))
            
    def on_fileChanged(self, filePath):
        if not os.path.exists(filePath):
            self.fileDeleted.emit(filePath)
        else:
            self.fileChanged.emit(filePath)
    
    def on_directoryChanged(self, directoryPath):
        if not os.path.exists(directoryPath):
            self.directoryDeleted.emit(directoryPath)
        else:
            self.directoryChanged.emit(directoryPath)
    
    def add_file_history(self, filePath):
        if filePath in self.fileHistory:
            self.fileHistory.remove(filePath)
        self.fileHistory.insert(0, filePath)
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
            raise PrymatexFileExistsException("The directory already exist", directory) 
        os.mkdir(directory)
    
    def createDirectories(self, directory):
        """Create a group of directory, one inside the other."""
        if os.path.exists(directory):
            raise PrymatexFileExistsException("The folder already exist", directory)
        os.makedirs(directory)
    
    def createFile(self, filePath):
        """Create a new file."""
        if os.path.exists(filePath):
            raise PrymatexIOException("The file already exist") 
        open(filePath, 'w').close()
    
    def renameFile(self, old, new):
        """Rename a file, changing its name from 'old' to 'new'."""
        if os.path.isfile(old):
            if os.path.exists(new):
                raise PrymatexFileExistsException(new)
            os.rename(old, new)
            return new
        return ''
    
    def renamePath(self, old, new):
        # According to http://docs.python.org/library/os.html
        # os.rename works with both dirs and files
        
        os.rename(old, new)
        self.closeFile(old)
        self.openFile(new)
        self.fileRenamed.emit(old, new)
        
    def deletePath(self, path):
        if os.path.isfile(path):
            # Mandar señal para cerrar editores
            os.unlink(path)
        else:
            shutil.rmtree(path)
    
    def fileExtension(self, filePath):
        """
        Get the file extension in the form of: 'py'
        """
        return os.path.splitext(filePath.lower())[-1][1:]
    
    def fileDirectory(self, filePath):
        """
        Get the file extension in the form of: 'py'
        """
        return os.path.dirname(filePath)
    
    def fileName(self, filePath):
        return os.path.basename(filePath)
    
    def mimeType(self, filePath):
        return mimetypes.guess_type(filePath)[0] or ""
        
    def isOpen(self, filePath):
        return filePath in self.fileWatcher.files()
    
    def openFile(self, filePath):
        """
        Open and read a file, return the content.
        """
        if not os.path.exists(filePath):
            raise PrymatexIOException("The file does not exist")
        if not os.path.isfile(filePath):
            raise PrymatexIOException("%s is not a file" % filePath)
        f = QtCore.QFile(filePath)
        if not f.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text):
            raise PrymatexIOException("%s" % f.errorString())
        stream = QtCore.QTextStream(f)
        content = stream.readAll()
        f.close()
        
        self.last_directory = os.path.dirname(filePath)
        #Update file history
        self.add_file_history(filePath)
        self.watchPath(filePath)
        return content

    def closeFile(self, filePath):
        self.unwatchPath(filePath)
        
    def saveFile(self, filePath, content):
        """
        Function that actually save the content of a file.
        """
        if self.isWatched(filePath):
            self.unwatchPath(filePath)
        try:
            f = QtCore.QFile(filePath)
            if not f.open(QtCore.QIODevice.WriteOnly | QtCore.QIODevice.Truncate):
                raise PrymatexIOException(f.errorString())
            stream = QtCore.QTextStream(f)
            encoded_stream = stream.codec().fromUnicode(content)
            f.write(encoded_stream)
            f.flush()
            f.close()
            self.watchPath(filePath)
        except:
            raise

    def isWatched(self, path):
        return path in self.fileWatcher.files() or path in self.fileWatcher.directories()
        
    def watchPath(self, path):
        self.logger.debug("Watch path %s" % path)
        self.fileWatcher.addPath(path)
    
    def unwatchPath(self, path):
        self.logger.debug("Unwatch path %s" % path)
        self.fileWatcher.removePath(path)
    
    def getDirectory(self, filePath = None):
        """
        Obtiene un directorio para el path
        """
        if filePath is None:
            #if fileInfo is None return the las directory or the home directory
            return self.last_directory
        if os.path.isdir(filePath):
            return filePath
        return os.path.dirname(filePath)

    def lastModification(self, filePath):
        return QtCore.QFileInfo(filePath).lastModified()

    def compareFiles(self, filePath1, filePath2, compareBy = "name"):
        value1, value2 = filePath1, filePath2
        if compareBy == "size":
            value1, value2 = os.path.getsize(filePath1), os.path.getsize(filePath2)
        elif compareBy == "date":
            value1, value2 = os.path.getctime(filePath1), os.path.getctime(filePath2)
        elif compareBy == "type":
            value1, value2 = self.fileExtension(filePath1), self.fileExtension(filePath2)
        return cmp(value1, value2)