#!/usr/bin/env python
#-*- encoding: utf-8 -*-


#Cosas interesantes
#http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qfilesystemwatcher.html

import os
import codecs
import shutil
import mimetypes
import fnmatch

from PyQt4 import QtCore, QtGui

from prymatex.utils import osextra
from prymatex.core.plugin import PMXBaseComponent
from prymatex.core.settings import pmxConfigPorperty
from prymatex.core import exceptions

class PMXFileManager(QtCore.QObject, PMXBaseComponent):
    """A File Manager"""
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
    
    ENCODINGS = ['windows-1253', 'iso-8859-7', 'macgreek']

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
    
    #========================================================
    # Signals
    #========================================================
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
    
    #========================================================
    # History
    #========================================================
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
    
    #========================================================
    # Path handling, create, move, copy, link, delete
    #========================================================
    def _onerror(func, path, exc_info):
        import stat
        if not os.access(path, os.W_OK):
            # Is the error an access error ?
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise
        
    def createDirectory(self, directory):
        """
        Create a new directory.
        """
        if os.path.exists(directory):
            raise exceptions.FileExistsException("The directory already exist", directory) 
        os.makedirs(directory)

    def createFile(self, filePath):
        """Create a new file."""
        if os.path.exists(filePath):
            raise exceptions.IOException("The file already exist") 
        open(filePath, 'w').close()
    
    move = lambda self, src, dst: shutil.move(src, dst)
    copytree = lambda self, src, dst: shutil.copytree(src, dst)
    copy = lambda self, src, dst: shutil.copy2(src, dst)
    link = lambda self, src, dst: dst

    def deletePath(self, path):
        if os.path.isfile(path):
            # Mandar señal para cerrar editores
            os.unlink(path)
        else:
            shutil.rmtree(path, onerror = self._onerror)
    
    #==================================================================
    # Path data
    #==================================================================
    extension = lambda self, path: os.path.splitext(path.lower())[-1][1:]
    splitext = lambda self, path: os.path.splitext(path)
    dirname = lambda self, path: os.path.dirname(path)
    basename = lambda self, path: os.path.basename(path)
    mimeType = lambda self, path: mimetypes.guess_type(path)[0] or ""

    #==================================================================
    # Handling files for retrieving data. open, read, write, close
    #==================================================================
    def isOpen(self, filePath):
        return filePath in self.fileWatcher.files()
    
    def openFile(self, filePath):
        """
        Open and read a file, return the content.
        """
        if not os.path.exists(filePath):
            raise exceptions.IOException("The file does not exist")
        if not os.path.isfile(filePath):
            raise exceptions.IOException("%s is not a file" % filePath)
        self.last_directory = os.path.dirname(filePath)
        #Update file history
        self.add_file_history(filePath)
        self.watchPath(filePath)

    def readFile(self, filePath):
        """Read from file"""
        #TODO: Que se pueda hacer una rutina usando yield
        for enc in [ self.encoding ] + self.ENCODINGS:
            try:
                fileRead = codecs.open(filePath, "r", encoding = enc)
                content = fileRead.read()
                break
            except Exception, e:
                print "File: %s, %s" % (filePath, e)
        fileRead.close()
        return content

    def writeFile(self, filePath, content):
        """Function that actually save the content of a file."""
        self.unwatchPath(filePath)
        fileWrite = codecs.open(filePath, "w", encoding = self.encoding)
        fileWrite.write(content)
        fileWrite.flush()
        fileWrite.close()
        self.watchPath(filePath)

    def closeFile(self, filePath):
        if self.isWatched(filePath):
            self.unwatchPath(filePath)

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

    def listDirectory(self, directory, absolute = False, filePatterns = []):
        if not os.path.isdir(directory):
            raise exceptions.DirectoryException("%s not exists" % directory)
        names = os.listdir(directory)
        if filePatterns:
            names = filter(lambda name: any(map(lambda pattern: os.path.isdir(os.path.join(directory, name)) or fnmatch.fnmatch(name, pattern), filePatterns)), names)
        if absolute:
            return map(lambda name: os.path.join(directory, name), names)
        return names

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