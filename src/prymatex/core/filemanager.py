'''
This module is inspired in QtCretor FileManager instance
'''

from PyQt4.QtCore import QObject, pyqtSignal, QString 
from PyQt4.QtCore import Qt
from prymatex.lib.magic import magic
from prymatex.core.base import PMXObject
from prymatex.core.config import Setting
from os.path import *
from prymatex.core.exceptions import APIUsageError, FileDoesNotExistError
import codecs

# TODO: Cross-platform implementation, you might not have rights to write
MAGIC_FILE = join(dirname(abspath(magic.__file__)), 'magic.linux')

class PMXFile(QObject):
    #===========================================================================
    # Signals
    #===========================================================================
    fileSaved = pyqtSignal(QString)
    fileRenamed = pyqtSignal(QString)
    fileSaveError = pyqtSignal(QString)
    
    _path = None
    
    BUFFER_SIZE = 2 << 20
    
    def __init__(self, parent, path = None):
        assert isinstance(parent, PMXFileManager), ("PMXFile should have a PMXFileManager"
                                                    "instance as parent. PMXFileManager is "
                                                    "a singleton property on "
                                                    "PMXApplication.file_manager")
        super(PMXFile, self).__init__(parent)
        self.path = path
        
    def suggestedFileName(self, editor_suffix = None):
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
                raise APIUsageError("Can't change file path from %s to %s" % (self._path, value))
            self._path  = value
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
        #f = open(self.path)
        f = codecs.open(self.path, 'r', 'utf-8')
        data = f.read()
        f.close()
        return data
#        for frm, to in zip(range(0, ), range()):
#            print frm, to
#            buffer[frm:to]
#            qApp.instance().processEvents()
    
    def __str__(self):
        return "<PMXFile on %s>" % self.path or "no path yet"

#    TODO: Check if we can implement this this as a generator
#    READ_SIZE = 1024 * 64 # 64K
#    def readFileContents(self, buffer):
#        '''
#        Reads file contents
#        '''
#        try:
#            size, read_count = os.path.getsize(self.path), 0
#            assert size > 0
#        except OSError:
#            logger.debug("Could not open %s", self.path)
#        except AssertionError:
#            logger.debug("Empty file")
#        else:
#            f = open(self.path, 'r')
#            while size > read_count :
#                content = f.read(self.READ_SIZE)
#                read_count += len(content)
#                self.codeEdit.insertPlainText(content)
#                #logger.debug("%d bytes read_count from %s", read_count, self.path)
#            f.close()
#            self.codeEdit.document().setModified(False)
#            self.codeEdit.document().setUndoRedoEnabled(True)
#        self.codeEdit.setEnabled(True)
#    

    
    __unicode__ = __repr__ = __str__
    
class PMXFileManager(PMXObject):
    '''
    A singleton which used for 
    '''
    
    filedOpened = pyqtSignal(PMXFile) # A new file has been opened
    
    class Meta:
        settings = 'core.filemanager'
    
    file_history = Setting(default = [])
    
    def __init__(self, parent):
        QObject.__init__(self, parent)
        
        self.magic = magic.Magic(MAGIC_FILE, 'delete-me')
        self.opened_files = {}
        self.empty_file_counter = 0 
    
    def isOpened(self, filepath):
        if filepath in self.opened_files:
            return True
        return False
    
    
    def getEmptyFile(self):
        ''' Returns a QFile '''
        pmx_file =  PMXFile(self)
        self.empty_file_counter += 1
        return pmx_file
    
    
    def openFile(self, filepath):
        '''
        PMXFile factory
        @raise FileDoesNotExistError: If provided path does not exists
        '''
        if self.isOpened(filepath):
            return self.opened_files[filepath]
        if not exists(filepath):
            raise FileDoesNotExistError(filepath)
        
        pmx_file = PMXFile(self, filepath)
        
        self.opened_files[filepath] = pmx_file
        self.filedOpened.emit(pmx_file)
        return pmx_file
    
    def recentFiles(self):
        return []
    