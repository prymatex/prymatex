'''
This module is inspired in QtCretor FileManager instance
'''

from PyQt4.QtCore import QObject, pyqtSignal, QString
from prymatex.lib.magic import magic
from prymatex.core.base import PMXObject
from prymatex.core.config import Setting
from os.path import *

MAGIC_FILE = join(dirname(abspath(magic.__file__)), 'magic.linux')
class PMXFile(QObject):
    #===========================================================================
    # Signals
    #===========================================================================
    fileChanged = pyqtSignal(QString)
    fileRenamed = pyqtSignal(QString)
    
    _path = None
    
    BUFFER_SIZE = 2 << 20
    
    def __init__(self, parent, path = None):
        assert isinstance(parent, PMXFileManager), ("PMXFile should have a PMXFileManager"
                                                    "instance as parent. PMXFileManager is "
                                                    "a singleton property on "
                                                    "PMXApplication.file_manager")
        super(PMXFile, self).__init__(parent)
        if path != None:
            self.path = self.path
        
    def suggestedFileName(self, editor_suffix = None):
        return "untitled"
    
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
        self._path = abspath(unicode(value))
        self.fileRenamed.emit('hoa')
    
    @property
    def filename(self):
        return basename(self.path)
    
    @property
    def directory(self):
        return dirname(self.path)
    
    @property
    def expect_file_changes(self):
        return self._expect_file_changes
        
    @expect_file_changes.setter
    def expect_file_changes(self, value):
        self._expect_file_changes = True
    
    
    def write(self, buffer):
        f = open(self.path, 'w')
        f.write(buffer)
        f.close()
        self.fileChanged.emit(self.path)
#        for frm, to in zip(range(0, ), range()):
#            print frm, to
#            buffer[frm:to]
#            qApp.instance().processEvents()
        
    
class PMXFileManager(PMXObject):
    '''
    A singleton which used for 
    '''
    class Meta:
        settings = 'core.filemanager'
    
    file_history = Setting(default = [])
    
    def __init__(self, parent):
        QObject.__init__(self, parent)
        
        self.magic = magic.Magic(MAGIC_FILE, 'delete-me')
    
    def getEmptyFile(self):
        ''' Returns a QFile '''
        return PMXFile(self)
    
    def openFiles(self, files):
        finstances = []
        for path in files:
            try:
                finstances.append(PMXFile(self, path))
            except Exception, _e:
                raise
            else:
                self.file_history.append(path)
                
        return finstances
            
    def recentFiles(self):
        return []
    