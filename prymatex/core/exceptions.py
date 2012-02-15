# coding: utf-8

from prymatex.utils.i18n import ugettext as _

class AlreadyRunningError(Exception):
    title = _('Application already running')

class UnsupportedPlatformError(Exception):
    pass
    
class APIUsageError(Exception):
    """
    Thrown when something is violating the way Prymatex is meant to be used
    """
    pass

class PrymatexIOException(Exception):
    pass

class PrymatexFileExistsException(PrymatexIOException):
    def __init__(self, msg, filePath = None):
        PrymatexIOException.__init__(self, msg)
        self.filePath = filePath

class PrymatexFileNotExistsException(PrymatexIOException):
    def __init__(self, msg, filePath = None):
        PrymatexIOException.__init__(self, msg)
        self.filePath = filePath
        
class PrymatexFilePermissionException(PrymatexIOException):
    pass

class PluginManagerException(Exception):
    pass
    
class FileNotSupported(Exception):
    pass
    
class UserCancelException(Exception):
    pass
