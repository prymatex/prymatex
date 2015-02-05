#!/usr/bin/env python
#-*- encoding: utf-8 -*-

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
    # ------------- Settings
    SETTINGS = 'FileManager'

    fileHistory = ConfigurableItem(default = [])
    fileHistoryLength = ConfigurableItem(default = 10)
    defaultEncoding = ConfigurableItem(default = 'utf_8')
    defaultEndOfLine = ConfigurableItem(default = 'unix')
    detectEndOfLine = ConfigurableItem(default = False)
    removeTrailingSpaces = ConfigurableItem(default = False)

    def __init__(self, **kwargs):
        super(FileManager, self).__init__(**kwargs)
        
        self.last_directory = get_home_dir()
        self._opens = []

    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.files import FilesSettingsWidget
        return [ FilesSettingsWidget ]

    # -------------- File Changes callbacks
    def _apply_callback(self, path):
        for callback in self.callbacks.get(path, []):
            callback(path)

    def add_change_callback(self, path, callback):
        callbacks = self.callbacks.setdefault(path, [])
        if callback not in callbacks:
            callbacks.append(callback)
        
    def remove_change_callback(self, path, callback):
        callbacks = self.callbacks.setdefault(path, [])
        if callback in callbacks:
            callbacks.remove(callback)
        
    # -------------- History
    def add_file_history(self, filePath):
        if filePath in self.fileHistory:
            self.fileHistory.remove(filePath)
        self.fileHistory.insert(0, filePath)
        if len(self.fileHistory) > self.fileHistoryLength:
            self.fileHistory = self.fileHistory[0:self.fileHistoryLength]
        self.settings().set("fileHistory", self.fileHistory)
    
    def clearFileHistory(self):
        self.fileHistory = []
        self.settings().set("fileHistory", self.fileHistory)
    
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
        return filePath in self._opens
    
    # ---------- Handling files for retrieving data. open, read, write, close
    def openFile(self, filePath):
        """Open and read a file, return the content.
        """
        if not os.path.exists(filePath):
            raise exceptions.IOException("The file does not exist: %s" % filePath)
        if not os.path.isfile(filePath):
            raise exceptions.IOException("%s is not a file" % filePath)
        self.last_directory = os.path.dirname(filePath)
        self.add_file_history(filePath)

    def readFile(self, filePath):
        """Read from file"""
        return encoding.read(filePath)

    def writeFile(self, filePath, content, encode=None):
        """Function that actually save the content of a file."""
        encode = encoding.write(content, filePath, encode or self.defaultEncoding)
        return encode

    def closeFile(self, filePath):
        pass

    def directory(self, filePath = None):
        """Obtiene un directorio para el path
        """
        if filePath is None:
            #if fileInfo is None return the las directory or the home directory
            return self.last_directory
        if os.path.isdir(filePath):
            return filePath
        return os.path.dirname(filePath)
    
    def listDirectory(self, directory, absolute=False, filePatterns=[]):
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
