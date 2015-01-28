#!/usr/bin/env python
#-*- encoding: utf-8 -*-

#TODO: MEJORAR LAS EXCEPTIONS

from prymatex.utils.i18n import ugettext as _

class PrymatexException(Exception):
    title = ''
    
    def __init__(self, message, *args):
        super(PrymatexException, self).__init__(*args)
        self.message = message

    def __str__(self):
        return "%s: %s" % (self.title, self.message)

class AlreadyRunningError(PrymatexException):
    title = _('Already running')

class UnsupportedPlatformError(PrymatexException):
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

class EnviromentNotSuitable(Exception):
    pass