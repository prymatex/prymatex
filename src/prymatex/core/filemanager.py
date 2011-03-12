'''
This module is inspired in QtCretor FileManager instance
'''

from PyQt4.QtCore import QObject
from prymatex.lib.magic import magic

class PMXFile(QObject):
    def __init__(self, path = None, parnet = None):
        pass


class PMXFileManager(QObject):
    '''
    A singleton which used for 
    '''
    def __init__(self, parent):
        QObject.__init__(self, parent)
        
    def openFiles(self, files):
        m = magic.Magic()
    
    def getEditorForFile(self):
        pass
    
    
    