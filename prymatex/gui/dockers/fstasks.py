#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.utils.i18n import ugettext as _
from prymatex.core import exceptions

class FileSystemTasks(object):
    """Groups FileSystem and Project actions, it's a facade of the PMXFileManager
    that displays dialogs and handle common exceptions.
    
    Slots Mixin
    """
    
    def createDirectory(self, directory):
        while True:
            newDirName, accepted = QtWidgets.QInputDialog.getText(self, _("Create Directory"), 
                                                        _("Please specify the new directory name"), 
                                                        text = _("New Folder"))
            if not accepted:
                break
            absNewDirName = os.path.join(directory, newDirName)
            try:
                self.application().fileManager.createDirectory(absNewDirName)
                return absNewDirName
            except exceptions.PrymatexFileExistsException as e:
                QtWidgets.QMessageBox.warning(self, _("Error creating directory"), 
                                          _("%s already exists") % newDirName)
            # Permissions? Bad Disk? 
            except Exception as e:
                # TODO: Show some info about the reason
                QtWidgets.QMessageBox.warning(self, _("Error creating directory"), 
                                          _("An error occured while creating %s") % newDirName)
    
    def createFile(self, directory):
        while True:
            newFileName, accepted = QtWidgets.QInputDialog.getText(self, _("Create file"), 
                                                        _("Please specify the file name"), 
                                                        text = _("NewFile"))
            if not accepted:
                break
        
            absNewFileName = os.path.join(directory, newFileName)
            try:
                self.application().fileManager.createFile(absNewFileName)
                return absNewFileName
            except exceptions.FileExistsException as e:
                QtWidgets.QMessageBox.warning(self, _("Error creating file"), _("%s already exists") % newFileName)
            except Exception as e:
                # TODO: Show some info about the reason
                QtWidgets.QMessageBox.warning(self, _("Error creating file"), 
                                          _("An error occured while creating %s") % absNewFileName)
    
    def deletePath(self, path):
        basePath, pathTail = os.path.split(path)
        result = QtWidgets.QMessageBox.question(self, _("Are you sure?"), 
                                        _("Are you sure you want to delete %s<br>"
                                          "This action can not be undone.") % pathTail,
                                            buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                            defaultButton = QtWidgets.QMessageBox.Cancel)
        if result == QtWidgets.QMessageBox.Ok:
            self.application().fileManager.deletePath(path)
            
    def renamePath(self, path):
        ''' Renames files and folders '''
        basePath, pathTail = os.path.split(path)
        if os.path.isdir(path):
            pathType = _('directory')
        elif os.path.isfile(path):
            pathType = _('file')
        while True:
            newName, accepted = QtWidgets.QInputDialog.getText(self, _("Choose new name for %s") % pathTail, 
                                                           _("Rename {0} {1}").format(pathType, pathTail),
                                                           text = pathTail)
            if accepted:
                if newName == pathTail:
                    continue # Same name
                newFullPath = os.path.join(basePath, newName)
                if os.path.exists(newFullPath):
                    rslt = QtWidgets.QMessageBox.warning(self, _("Destination already exists"), 
                                              _("{0} already exists").format(newName), 
                                                buttons=QtWidgets.QMessageBox.Retry | QtWidgets.QMessageBox.Cancel,
                                                defaultButton=QtWidgets.QMessageBox.Retry)
                    if rslt == QtWidgets.QMessageBox.Cancel:
                        return
                    continue
                self.application().fileManager.move(path, newFullPath)
                return newFullPath
            else:
                return 
            
