#!/usr/bin/env python
#-*- encoding: utf-8 -*-

#TODO: MEJORAR LAS EXCEPTIONS

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

class IOException(Exception):
    pass

class FileException(IOException):
    def __init__(self, msg, filePath = None):
        IOException.__init__(self, msg)
        self.filePath = filePath

class FileExistsException(FileException):
    pass

class FileNotExistsException(FileException):
    pass
        
class FilePermissionException(IOException):
    pass

class DirectoryException(IOException):
    def __init__(self, msg, directory = None):
        IOException.__init__(self, msg)
        self.directory = directory

class PluginManagerException(Exception):
    pass
    
class FileNotSupported(Exception):
    pass
    
class UserCancelException(Exception):
    pass

class LocationIsNotProject(Exception):
    pass

class ProjectExistsException(Exception):
    pass