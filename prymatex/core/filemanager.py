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

    def openFile(self, fileInfo):
        return QtCore.QFile(fileInfo.absoluteFilePath())
    
    def saveFile(self, fileInfo, data):
        file = QtCore.QFile(fileInfo.absoluteFilePath())
        file.open()
        file.write(data)
    
    @property
    def currentDirectory(self):
        #TODO: el ultimo directorio o algo de eso :)
        return os.path.expanduser("~") 

    def getEmptyFile(self):
        ''' Returns a QFile '''
        path = os.path.join(self.currentDirectory, "untitled %d" % self.empty_file_counter)
        self.empty_file_counter += 1
        return QtCore.QFileInfo(path)
        
    def getOpenFiles(self):
        names = QtGui.QFileDialog.getOpenFileNames(None, "Open Files", self.currentDirectory)
        files = map(lambda name: QtCore.QFileInfo(name), names)
        names.reverse()
        self.fileHistory = names + self.fileHistory
        if len(self.fileHistory) > self.fileHistoryLength:
            self.fileHistory = self.fileHistory[0:self.fileHistoryLength]
        self.fileHistoryChanged.emit()
        return files
    
    def getSaveFile(self, title = "Save file"):
        name = QtGui.QFileDialog.getSaveFileName(None, title, "", "")
        return QtCore.QFileInfo(name)
    
    def getFileIcon(self, fileInfo):
        if fileInfo.exists():
            return self.iconProvider.icon(fileInfo)
        return self.iconProvider.icon(QtGui.QFileIconProvider.File)
