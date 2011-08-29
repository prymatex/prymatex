'''
This module is inspired in QtCretor FileManager instance
'''

import os, codecs
from PyQt4 import QtCore, QtGui
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.core.exceptions import APIUsageError, FileDoesNotExistError

class PMXFileManager(PMXObject):
    ''' A File Manager
    '''
    fileOpened = QtCore.pyqtSignal()
    fileHistoryChanged = QtCore.pyqtSignal()
    
    class Meta:
        settings = 'filemanager'

    fileHistory = pmxConfigPorperty(default=[])
    fileHistoryLength = pmxConfigPorperty(default=10)

    def __init__(self, parent):
        super(PMXFileManager, self).__init__(parent)

        self.opened_files = {}
        self.empty_file_counter = 0
        self.iconProvider = QtGui.QFileIconProvider()
        self.configure()

    def fileUnused(self):
        ''' Signal receiver for '''
        pmx_file = self.sender()
        print self.opened_files
        if pmx_file.path:
            pmx_file = self.opened_files.pop(pmx_file.path)
            del pmx_file

    def openFile(self, file):
        '''
        PMXFile factory
        @raise FileDoesNotExistError: If provided path does not exists
        '''
        if self.isOpened(filepath):
            pmx_file = self.opened_files[filepath]
            pmx_file.references += 1
            return self.opened_files[filepath]
        if not os.path.exists(filepath):
            raise FileDoesNotExistError(filepath)

        pmx_file = PMXFile(self, filepath)
        pmx_file.references += 1
        self.opened_files[filepath] = pmx_file
        self.fileOpened.emit(pmx_file)
        return pmx_file

    @property
    def currentDirectory(self):
        #TODO: el ultimo directorio o algo de eso :)
        return os.path.expanduser("~") 

    def getEmptyFile(self):
        ''' Returns a QFile '''
        path = os.path.join(self.currentDirectory, "untitled %d" % self.empty_file_counter)
        self.empty_file_counter += 1
        return QtCore.QFile(path)
        
    def getOpenFiles(self):
        names = QtGui.QFileDialog.getOpenFileNames(None, "Open Files", self.currentDirectory)
        files = map(lambda name: QtCore.QFile(name), names)
        names.reverse()
        self.fileHistory = names + self.fileHistory
        if len(self.fileHistory) > self.fileHistoryLength:
            self.fileHistory = self.fileHistory[0:self.fileHistoryLength]
        self.fileHistoryChanged.emit()
        return files

    def getFileIcon(self, file):
        info = QtCore.QFileInfo(file.path)
        if info.exists():
            return self.iconProvider.icon(info)
        return self.iconProvider.icon(QtGui.QFileIconProvider.File)
