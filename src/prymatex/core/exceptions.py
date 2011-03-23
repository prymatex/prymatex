# coding: utf-8

def _(m):
    from PyQt4.QtGui import qApp
    return unicode(qApp.instance().trUtf8(m))

class APIUsageError(Exception):
    '''
    Thrown when something is violating the way Prymatex is meant to be
    used
    '''
    pass

class FileDoesNotExistError(Exception):
    def __init__(self, path):
        self.path = path
        super(FileDoesNotExistError, self).__init__(_("%s does not exist") % path)
        
    