'''
This module is inspired in QtCretor FileManager instance
'''

from PyQt4 import QtCore 
from prymatex.utils.magic import magic
from prymatex.core.base import PMXObject
from prymatex.core.config import pmxConfigPorperty
from prymatex.core.exceptions import APIUsageError, FileDoesNotExistError
import os, codecs

from logging import getLogger
logger = getLogger(__file__)

# TODO: Cross-platform implementation, you might not have rights to write
MAGIC_FILE = os.path.join(os.path.dirname(os.path.abspath(magic.__file__)), 'magic.linux')


class PMXFile(QtCore.QObject):
    #==========================================================================
    # Signals
    #==========================================================================
    fileSaved = QtCore.pyqtSignal(str)
    fileRenamed = QtCore.pyqtSignal(str)
    fileSaveError = QtCore.pyqtSignal(str)
    fileLostReference = QtCore.pyqtSignal()

    _path = None
    _references = 0

    BUFFER_SIZE = 2 << 20

    def __init__(self, parent, path=None):
        assert isinstance(parent, PMXFileManager), ("PMXFile should have a "
        "PMXFileManager instance as parent. PMXFileManager is a singleton"
        " property on PMXApplication.fileManager")
        super(PMXFile, self).__init__(parent)
        self.path = path
        self.fileLostReference.connect(parent.fileUnused)
        self.destroyed.connect(self.fileDestroyed)

    @property
    def references(self):
        return self._references

    @references.setter
    def references(self, value):
        assert type(value) in (int, )
        self._references = value
        if self._references == 0:
            self.fileLostReference.emit()

    def suggestedFileName(self, editor_suffix=None):
        title = unicode(self.trUtf8("Untitled file %d"))
        return  title % self.parent().empty_file_counter

    @property
    def mtime(self):
        ''' File mtime '''
        if not self.path:
            return None
        raise NotImplementedError("")

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if value is None:
            if self._path:
                raise APIUsageError("Can't change file path from %s to %s" %
                (self._path, value))
            self._path = value
        else:
            abs_path = abspath(unicode(value))
            self._path = abs_path
            self.fileRenamed.emit(abs_path)

    @property
    def filename(self):
        if not self.path:
            return self.suggestedFileName()
        return basename(self.path)

    @property
    def directory(self):
        return dirname(self.path)

    # Taken from Qt creator, it should disable some modification signals
    @property
    def expect_file_changes(self):
        return self._expect_file_changes

    @expect_file_changes.setter
    def expect_file_changes(self, value):
        self._expect_file_changes = True

    def write(self, buffer):
        try:
            #f = open(self.path, 'w')
            f = codecs.open(self.path, 'w', 'utf-8')
        except IOError, e:
            self.fileSaveError(str(e))
        f.write(buffer)
        f.close()
        self.fileSaved.emit(self.path)

    def read(self):
        if not self.path:
            return None
        f = codecs.open(self.path, 'r', 'utf-8')
        data = f.read()
        f.close()
        return data
    
    def fileDestroyed(self):
        logger.debug("%s is being destoyed")

    def __str__(self):
        return "<PMXFile on %s>" % self.path or "no path yet"

    __unicode__ = __repr__ = __str__
    

class PMXFileManager(PMXObject):
    ''' A File Manager singleton
    '''
    fileOpened = QtCore.pyqtSignal(PMXFile)

    class Meta:
        settings = 'filemanager'

    file_history = pmxConfigPorperty(default=[])

    def __init__(self, parent):
        super(PMXFileManager, self).__init__(parent)

        self.magic = magic.Magic(MAGIC_FILE, os.path.join(self.pmxApp.settings.PMX_TMP_PATH, 'magic.cache'))
        self.opened_files = {}
        self.empty_file_counter = 0

    def isOpened(self, filepath):
        filepath = abspath(filepath)
        if filepath in self.opened_files:
            return True
        return False


    def getEmptyFile(self):
        ''' Returns a QFile '''
        pmx_file =  PMXFile(self)
        self.empty_file_counter += 1
        pmx_file.references = 1
        return pmx_file


    def fileUnused(self):
        ''' Signal receiver for '''
        pmx_file = self.sender()
        print self.opened_files
        if pmx_file.path:
            pmx_file = self.opened_files.pop(pmx_file.path)
            del pmx_file


    def openFile(self, filepath):
        '''
        PMXFile factory
        @raise FileDoesNotExistError: If provided path does not exists
        '''
        if self.isOpened(filepath):
            pmx_file = self.opened_files[filepath]
            pmx_file.references += 1
            return self.opened_files[filepath]
        if not exists(filepath):
            raise FileDoesNotExistError(filepath)

        pmx_file = PMXFile(self, filepath)
        pmx_file.references += 1
        self.opened_files[filepath] = pmx_file
        self.filedOpened.emit(pmx_file)

        return pmx_file

    @property
    def currentDirectory(self):
        #TODO: el ultimo directorio o algo de eso :)
        return os.path.expanduser("~") 
    
    def recentFiles(self):
        return []
