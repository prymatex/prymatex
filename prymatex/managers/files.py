#!/usr/bin/env python
#-*- encoding: utf-8 -*-


#Cosas interesantes
#http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qfilesystemwatcher.html

import os
import codecs
import shutil
import mimetypes
import fnmatch

from prymatex.qt import QtCore, QtGui

from prymatex.utils import osextra
from prymatex.utils.decorators import deprecated
from prymatex.utils import encoding

from prymatex.core import PrymatexComponent
from prymatex.core.settings import ConfigurableItem
from prymatex.utils.misc import get_home_dir
from prymatex.core import exceptions

class FileManager(PrymatexComponent, QtCore.QObject):
    """A File Manager"""
    # ------------ Signals
    fileCreated = QtCore.Signal(str)
    fileDeleted = QtCore.Signal(str)
    fileChanged = QtCore.Signal(str)
    fileRenamed = QtCore.Signal(str, str)
    directoryCreated = QtCore.Signal(str)
    directoryDeleted = QtCore.Signal(str)
    directoryChanged = QtCore.Signal(str)
    directoryRenamed = QtCore.Signal(str, str)

    # Generic Signal 
    fileSytemChanged = QtCore.Signal(str, int)

    # ------------- Settings
    SETTINGS = 'FileManager'

    fileHistory = ConfigurableItem(default = [])
    fileHistoryLength = ConfigurableItem(default = 10)
    defaultEncoding = ConfigurableItem(default = 'utf_8')
    defaultEndOfLine = ConfigurableItem(default = 'unix')
    detectEndOfLine = ConfigurableItem(default = False)
    removeTrailingSpaces = ConfigurableItem(default = False)

    # ---------------- Constants
    CREATED = 1<<0
    DELETED = 1<<1
    RENAMED = 1<<2
    MOVED   = 1<<3
    CHANGED = 1<<4

    def __init__(self, **kwargs):
        super(FileManager, self).__init__(**kwargs)
        
        self.last_directory = get_home_dir()
        self.fileWatcher = QtCore.QFileSystemWatcher()
        self.fileWatcher.fileChanged.connect(self.on_fileWatcher_fileChanged)
        self.fileWatcher.directoryChanged.connect(self.on_fileWatcher_directoryChanged)
        self.connectGenericSignal()

    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.files import FilesSettingsWidget
        return [ FilesSettingsWidget ]
    
    # ------------- Signals
    def connectGenericSignal(self):
        UNARY_SINGAL_CONSTANT_MAP = (
            (self.fileCreated, FileManager.CREATED ),
            (self.fileDeleted, FileManager.DELETED ),
            (self.fileChanged, FileManager.CHANGED ),
            (self.directoryCreated, FileManager.CREATED ),
            (self.directoryDeleted, FileManager.DELETED ),
            (self.directoryChanged, FileManager.CHANGED ),
        )
        BINARY_SINGAL_CONSTANT_MAP = (
            (self.fileRenamed, FileManager.RENAMED ),
            (self.directoryRenamed, FileManager.RENAMED ),                       
        )
        for signal, associatedConstant in UNARY_SINGAL_CONSTANT_MAP:
            signal.connect(lambda path, constant = associatedConstant: self.fileSytemChanged.emit(path, constant))
        for signal, associatedConstant in BINARY_SINGAL_CONSTANT_MAP:
            signal.connect(lambda _x, path, constant = associatedConstant: self.fileSytemChanged.emit(path, constant))

    def on_fileWatcher_fileChanged(self, filePath):
        if not os.path.exists(filePath):
            self.fileDeleted.emit(filePath)
        else:
            self.fileChanged.emit(filePath)
    
    def on_fileWatcher_directoryChanged(self, directoryPath):
        if not os.path.exists(directoryPath):
            self.directoryDeleted.emit(directoryPath)
        else:
            self.directoryChanged.emit(directoryPath)
    
    # -------------- History
    def add_file_history(self, filePath):
        if filePath in self.fileHistory:
            self.fileHistory.remove(filePath)
        self.fileHistory.insert(0, filePath)
        if len(self.fileHistory) > self.fileHistoryLength:
            self.fileHistory = self.fileHistory[0:self.fileHistoryLength]
        self._settings.setValue("fileHistory", self.fileHistory)
    
    def clearFileHistory(self):
        self.fileHistory = []
        self._settings.setValue("fileHistory", self.fileHistory)
    
    #========================================================
    # Path handling, create, move, copy, link, delete
    #========================================================
    def _onerror(func, path, exc_info): #@NoSelf
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
            # Send signal for close editors
            os.unlink(path)
        else:
            shutil.rmtree(path, onerror = self._onerror)
    
    #==================================================================
    # Path data
    #==================================================================
    exists = lambda self, path: os.path.exists(path)
    isdir = lambda self, path: os.path.isdir(path)
    isfile = lambda self, path: os.path.isfile(path)
    islink = lambda self, path: os.path.islink(path)
    ismount = lambda self, path: os.path.ismount(path)
    join = lambda self, *path: os.path.join(*path)
    extension = lambda self, path: os.path.splitext(path.lower())[-1][1:]
    splitext = lambda self, path: os.path.splitext(path)
    dirname = lambda self, path: os.path.dirname(path)
    basename = lambda self, path: os.path.basename(path)
    mimeType = lambda self, path: mimetypes.guess_type(path)[0] or ""
    issubpath = lambda self, childPath, parentPath, **kwargs: osextra.path.issubpath(childPath, parentPath, **kwargs)
    fullsplit = lambda self, path: osextra.path.fullsplit(path)
    normcase = lambda self, path: os.path.normcase(path)
    normpath = lambda self, path: os.path.normpath(path)
    realpath = lambda self, path: os.path.realpath(path)
    relpath = lambda self, path: os.path.relpath(path)
    samefile = lambda self, path1, path2: os.path.samefile(path1, path2)
    fnmatch = lambda self, filename, pattern: fnmatch.fnmatch(filename, pattern)
    getmtime = lambda self, path: os.path.getmtime(path)
    getctime = lambda self, path: os.path.getctime(path)

    def expandVars(self, text):
        context = self.application().supportManager.environmentVariables()
        path = osextra.path.expand_shell_variables(text, context = context)
        if os.path.exists(path):
            return path
    
    def fnmatchany(self, filename, patterns):
        return any([fnmatch.fnmatch(filename, pattern) for pattern in patterns])

    # -------------- Open file control
    def isOpen(self, filePath):
        return filePath in self.fileWatcher.files()
    
    def isWatched(self, path):
        return path in self.fileWatcher.files() or path in self.fileWatcher.directories()
        
    def watchPath(self, path):
        self.logger().debug("Watch path %s" % path)
        self.fileWatcher.addPath(path)
    
    def unwatchPath(self, path):
        self.logger().debug("Unwatch path %s" % path)
        self.fileWatcher.removePath(path)
    
    # ---------- Handling files for retrieving data. open, read, write, close
    def openFile(self, filePath):
        """
        Open and read a file, return the content.
        """
        if not os.path.exists(filePath):
            raise exceptions.IOException("The file does not exist: %s" % filePath)
        if not os.path.isfile(filePath):
            raise exceptions.IOException("%s is not a file" % filePath)
        self.last_directory = os.path.dirname(filePath)
        #Update file history
        self.add_file_history(filePath)
        self.watchPath(filePath)

    def readFile(self, filePath):
        """Read from file"""
        content, encode = encoding.read(filePath)
        return content

    def writeFile(self, filePath, content):
        """Function that actually save the content of a file."""
        self.unwatchPath(filePath)
        encode = encoding.write(content, filePath, self.defaultEncoding)
        self.watchPath(filePath)

    def closeFile(self, filePath):
        if self.isWatched(filePath):
            self.unwatchPath(filePath)

    def directory(self, filePath = None):
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
        filenames = os.listdir(directory)
        if filePatterns:
            filenames = [filename for filename in filenames if os.path.isdir(os.path.join(directory, filename)) or\
                    self.fnmatchany(filename, filePatterns)]
        if absolute:
            return [os.path.join(directory, name) for name in filenames]
        return filenames

    def lastModification(self, filePath):
        return QtCore.QFileInfo(filePath).lastModified()

    def compareFiles(self, filePath1, filePath2, compareBy = "name"):
        value1, value2 = filePath1, filePath2
        if compareBy == "size":
            value1, value2 = os.path.getsize(filePath1), os.path.getsize(filePath2)
        elif compareBy == "date":
            value1, value2 = os.path.getctime(filePath1), os.path.getctime(filePath2)
        elif compareBy == "type":
            _, value1 = os.path.splitext(filePath1)
            _, value2 = os.path.splitext(filePath2)
        return (value1 > value2) - (value1 < value2)
