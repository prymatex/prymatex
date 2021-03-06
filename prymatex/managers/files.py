#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import codecs
import shutil
import mimetypes

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.extensions import CheckableMessageBox, ReplaceRenameInputDialog

from prymatex.core import config
from prymatex.core import PrymatexComponent
from prymatex.core.settings import ConfigurableItem
from prymatex.core import notifier
from prymatex.core import exceptions

from prymatex.utils.i18n import ugettext as _
from prymatex.utils import osextra
from prymatex.utils.decorators import deprecated
from prymatex.utils import encoding
from prymatex.utils import fnmatch

class FileManager(PrymatexComponent, QtCore.QObject):
    #Signals
    openFileChanged = QtCore.Signal(str)
    
    #Configuration
    file_history_length = ConfigurableItem(default=10)
    default_encoding = ConfigurableItem(default='utf_8')
    default_end_of_line = ConfigurableItem(default='unix')
    detect_end_of_line = ConfigurableItem(default=False)
    remove_trailing_spaces = ConfigurableItem(default=False)

    def __init__(self, **kwargs):
        super(FileManager, self).__init__(**kwargs)
        self.last_directory = config.USER_HOME_PATH
        self.file_history = []
        self.fileSystemWatcher = QtCore.QFileSystemWatcher()
        self.fileSystemWatcher.fileChanged.connect(self.openFileChanged.emit)

    @classmethod
    def contributeToSettings(cls):
        from prymatex.gui.settings.files import FilesSettingsWidget
        return [ FilesSettingsWidget ]

    # ---------- OVERRIDE: PrymatexComponent.componentState()
    def componentState(self):
        componentState = super(FileManager, self).componentState()

        componentState["file_history"] = self.file_history
        return componentState

    # ---------- OVERRIDE: PrymatexComponent.setComponentState()
    def setComponentState(self, componentState):
        super(FileManager, self).setComponentState(componentState)
        
        # Restore file history
        self.file_history = componentState.get("file_history", [])

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
    def add_file_history(self, file_path):
        if file_path in self.file_history:
            self.file_history.remove(file_path)
        self.file_history.insert(0, file_path)
        if len(self.file_history) > self.file_history_length:
            self.file_history = self.file_history[0:self.file_history_length]
    
    def clearFileHistory(self):
        self.file_history = []
    
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
        """Create a new directory."""
        if os.path.exists(directory):
            raise exceptions.FileExistsException("The directory already exist", directory) 
        os.makedirs(directory)

    def createFile(self, file_path):
        """Create a new file.
        """
        if os.path.exists(file_path):
            raise exceptions.IOException("The file already exist") 
        open(file_path, 'w').close()
    
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
    
    # Path data
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
    commonpath = lambda self, *args, **kwargs: osextra.path.commonpath(*args, **kwargs)
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
    
    # ---------- Handling files for retrieving data. open, read, write, close
    def openFile(self, file_path):
        """Open and read a file, return the content.
        """
        if not os.path.exists(file_path):
            raise exceptions.IOException("The file does not exist: %s" % file_path)
        if not os.path.isfile(file_path):
            raise exceptions.IOException("%s is not a file" % file_path)
        self.last_directory = os.path.dirname(file_path)
        self.add_file_history(file_path)
        self.fileSystemWatcher.addPath(file_path)

    def readFile(self, file_path):
        """Read from file"""
        return encoding.read(file_path)

    def writeFile(self, file_path, content, encode=None):
        """Function that actually save the content of a file."""
        self.fileSystemWatcher.removePath(file_path)
        encode = encoding.write(content, file_path, encode or self.defaultEncoding)
        self.fileSystemWatcher.addPath(file_path)
        return encode

    def closeFile(self, file_path):
        self.fileSystemWatcher.removePath(file_path)

    def directory(self, file_path = None):
        """Obtiene un directorio para el path
        """
        if file_path is None:
            #if fileInfo is None return the las directory or the home directory
            return self.last_directory
        if os.path.isdir(file_path):
            return file_path
        return os.path.dirname(file_path)
    
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

    def compareFiles(self, filePath1, filePath2, compareBy="name"):
        value1, value2 = filePath1, filePath2
        if compareBy == "size":
            value1, value2 = os.path.getsize(filePath1), os.path.getsize(filePath2)
        elif compareBy == "date":
            value1, value2 = os.path.getctime(filePath1), os.path.getctime(filePath2)
        elif compareBy == "type":
            _, value1 = os.path.splitext(filePath1)
            _, value2 = os.path.splitext(filePath2)
        return (value1 > value2) - (value1 < value2)

    def createDirectoryDialog(self, directory, widget=None):
        while True:
            newDirName, accepted = QtWidgets.QInputDialog.getText(widget, _("Create Directory"), 
                                                        _("Please specify the new directory name"), 
                                                        text = _("New Folder"))
            if not accepted:
                break
            absNewDirName = os.path.join(directory, newDirName)
            try:
                self.createDirectory(absNewDirName)
                return absNewDirName
            except exceptions.PrymatexFileExistsException as e:
                QtWidgets.QMessageBox.warning(widget, _("Error creating directory"), 
                                          _("%s already exists") % newDirName)
            # Permissions? Bad Disk? 
            except Exception as e:
                # TODO: Show some info about the reason
                QtWidgets.QMessageBox.warning(widget, _("Error creating directory"), 
                                          _("An error occured while creating %s") % newDirName)
    
    def createFileDialog(self, directory, widget=None):
        while True:
            newFileName, accepted = QtWidgets.QInputDialog.getText(widget, _("Create file"), 
                                                        _("Please specify the file name"), 
                                                        text = _("NewFile"))
            if not accepted:
                break
        
            absNewFileName = os.path.join(directory, newFileName)
            try:
                self.createFile(absNewFileName)
                return absNewFileName
            except exceptions.FileExistsException as e:
                QtWidgets.QMessageBox.warning(widget, _("Error creating file"), _("%s already exists") % newFileName)
            except Exception as e:
                # TODO: Show some info about the reason
                QtWidgets.QMessageBox.warning(widget, _("Error creating file"), 
                                          _("An error occured while creating %s") % absNewFileName)
    
    def deletePathDialog(self, path, widget=None):
        basePath, pathTail = os.path.split(path)
        result = QtWidgets.QMessageBox.question(widget, _("Are you sure?"), 
                                        _("Are you sure you want to delete %s<br>"
                                          "This action can not be undone.") % pathTail,
                                            buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                            defaultButton = QtWidgets.QMessageBox.Cancel)
        if result == QtWidgets.QMessageBox.Ok:
            self.deletePath(path)
            
    def renamePathDialog(self, path, widget=None):
        ''' Renames files and folders '''
        basePath, pathTail = os.path.split(path)
        if os.path.isdir(path):
            pathType = _('directory')
        elif os.path.isfile(path):
            pathType = _('file')
        while True:
            newName, accepted = QtWidgets.QInputDialog.getText(widget, _("Choose new name for %s") % pathTail, 
                                                           _("Rename {0} {1}").format(pathType, pathTail),
                                                           text = pathTail)
            if accepted:
                if newName == pathTail:
                    continue # Same name
                newFullPath = os.path.join(basePath, newName)
                if os.path.exists(newFullPath):
                    rslt = QtWidgets.QMessageBox.warning(widget, _("Destination already exists"), 
                                              _("{0} already exists").format(newName), 
                                                buttons=QtWidgets.QMessageBox.Retry | QtWidgets.QMessageBox.Cancel,
                                                defaultButton=QtWidgets.QMessageBox.Retry)
                    if rslt == QtWidgets.QMessageBox.Cancel:
                        return
                    continue
                self.move(path, newFullPath)
                return newFullPath
            else:
                return
    
    def copyPathDialog(self, srcPath, dstPath, widget=None, override=False):
        ''' Copy files and folders '''
        basename = self.basename(dstPath)
        dirname = self.dirname(dstPath)
        while not override and self.exists(dstPath):
            basename, ret = ReplaceRenameInputDialog.getText(widget, _("Already exists"), 
                _("Destiny already exists\nReplace or or replace?"), text = basename, )
            if ret == ReplaceRenameInputDialog.Cancel: return
            if ret == ReplaceRenameInputDialog.Replace: break
            dstPath = os.path.join(dirname, basename)
        if os.path.isdir(srcPath):
            self.copytree(srcPath, dstPath)
        else:
            self.copy(srcPath, dstPath)
