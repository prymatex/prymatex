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
    
    def __init__(self, parent, path = None):
        assert isinstance(parent, PMXFileManager), ("PMXFile should have a PMXFileManager"
                                                    "instance as parent. PMXFileManager is "
                                                    "a singleton property on "
                                                    "PMXApplication.file_manager")
        QObject.__init__(parent)
        self.path = self.path
        
    def suggestedFileName(self, editor_suffix = None):
        return "Untitled file"
    
    @property
    def mtime(self):
        ''' File mtime '''
        if not self.path:
            return None
        raise NotImplementedError("")
    
    @property
    def path(self):
        return self.path
    
    @path.setter
    def path(self, value):
        self.path = value
        self.pathChange.emit(value)
        
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
    