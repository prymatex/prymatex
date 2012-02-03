import os

from PyQt4 import QtGui, QtCore

from prymatex.utils.i18n import ugettext as _
from prymatex.core.exceptions import PrymatexFileExistsException
from prymatex.gui.dialogs.newfromtemplate import PMXNewFromTemplateDialog

class PMXFileSystemTasks(object):
    '''
    Groups FileSystem and Project actions, it's a facade of the PMXFileManager
    that displays dialogs and handle common exceptions.
    
    Slots Mixin
    '''
    
    def createDirectory(self, basePath):
        if not os.path.isdir(basePath):
            # If base is a file, we should take its parent dir
            basePath = os.path.dirname(basePath)
        while True:
            newDirName, accepted = QtGui.QInputDialog.getText(self, _("Create Directory"), 
                                                        _("Please specify the new directory name"), 
                                                        text = _("New Folder"))
            if accepted:
                absNewDirName = os.path.join(basePath, newDirName)
                try:
                    rslt = self.application.fileManager.createDirectory(absNewDirName)
                except PrymatexFileExistsException as e:
                    QtGui.QMessageBox.warning(self, _("Error creating directory"), 
                                              _("%s already exists") % newDirName)
                    continue
                # Permissions? Bad Disk? 
                except Exception as e:
                    # TODO: Show some info about the reason
                    QtGui.QMessageBox.warning(self, _("Error creating directory"), 
                                              _("An error occured while creating %s") % newDirName)
                    
                else:
                    break
            else:
                return
    
    def createFile(self, basePath):
        while True:
            newFileName, accepted = QtGui.QInputDialog.getText(self, _("Create file"), 
                                                        _("Please specify the file name"), 
                                                        text = _("NewFile"))
            if accepted:
                absNewFileName = os.path.join(basePath, newFileName)
                try:
                    rslt = self.application.fileManager.createFile(absNewFileName)
                except PrymatexFileExistsException as e:
                    QtGui.QMessageBox.warning(self, _("Error creating file"), 
                                              _("%s already exists") % newFileName)
                    continue
                # Permissions? Bad Disk? 
                except Exception as e:
                    # TODO: Show some info about the reason
                    QtGui.QMessageBox.warning(self, _("Error creating file"), 
                                              _("An error occured while creating %s") % absNewFileName)
                    
                else:
                    print("Created", rslt)
                    break
            else:
                return
    
    def createFileFromTemplate(self, basePath):
        fileDirectory = self.application.fileManager.getDirectory(basePath)
        return PMXNewFromTemplateDialog.newFileFromTemplate(fileDirectory = fileDirectory,  parent = self)
    
    def deletePath(self, path):
        basePath, pathTail = os.path.split(path)
        result = QtGui.QMessageBox.question(self, _("Are you sure?"), 
                                        _("Are you sure you want to delete %s<br>"
                                          "This action can not be undone.") % pathTail,
                                            buttons = QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                                            defaultButton = QtGui.QMessageBox.Cancel)
        if result == QtGui.QMessageBox.Ok:
            self.application.fileManager.deletePath(path)
            
    def renamePath(self, path):
        ''' Renames files and folders '''
        basePath, pathTail = os.path.split(path)
        if os.path.isdir(path):
            pathType = _('directory')
        elif os.path.isfile(path):
            pathType = _('file')
        while True:
            newName, accepted = QtGui.QInputDialog.getText(self, 
                                                           _("Choose new name for %s") % pathTail, 
                                                           _("Rename {0} {1}").format(pathType, pathTail),
                                                           text = pathTail)
            
            if accepted:
                if newName == pathTail:
                    continue # Same name
                newFullPath = os.path.join(basePath, newName)
                if os.path.exists(newFullPath):
                    rslt = QtGui.QMessageBox.warning(self, _("Destination already exists"), 
                                              _("{0} already exists").format(newName), 
                                                buttons=QtGui.QMessageBox.Retry | QtGui.QMessageBox.Cancel,
                                                defaultButton=QtGui.QMessageBox.Retry)
                    if rslt == QtGui.QMessageBox.Cancel:
                        return
                    continue
                self.application.fileManager.renamePath(path, newFullPath)
                return newFullPath
            else:
                return 
            