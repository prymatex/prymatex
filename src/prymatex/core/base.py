#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class PMXOptions(object):
    def __init__(self, options):
        self.settings = QtGui.QApplication.instance().settings.getGroup(getattr(options, 'settings', ''))

class PMXObjectBase(QtCore.pyqtWrapperType):
    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')
        new_class = super(PMXObjectBase, cls).__new__(cls, name, bases, { '__module__': module })
        opts = PMXOptions(attrs.get('Meta', None))
        new_class.add_to_class('_meta', opts)
        for name, attr in attrs.iteritems():
            new_class.add_to_class(name, attr)
        return new_class

    def add_to_class(cls, name, value): #@NoSelf
        if hasattr(value, 'contributeToClass'):
            value.contributeToClass(cls, name)
        else:
            setattr(cls, name, value)

from logging import getLogger

class PMXObject(QtCore.QObject):
    __metaclass__ = PMXObjectBase
    __app = QtGui.QApplication.instance()
    __mainwindow = None
    __logger = None
    
    def __del__(self):
        self._meta.settings.removeListener(self)

    #============================================================
    # Settings
    #============================================================
    def configure(self):
        self._meta.settings.addListener(self)
        self._meta.settings.configure(self)
    
    # Shortcuts
    def settingsValue(self, name, default = None):
        ''' A shortcut, for access to root settings
            Usage: 
                Accesss to Bar group
                PMXObjectInstance.settingsValue("Bar/settingsAttribute");
                PMXObjectInstance.settingsValue("Bar/settingsAttribute", default = "foo");
                Accesss to Global group
                PMXObjectInstance.settingsValue("settingsAttribute", default = "foo");
        '''
        value = self.pmxApp.settings.value(name)
        value = value if value != None else default
        return value
    
    def setSettingsValue(self, name, value):
        ''' A shortcut, for access to root settings
            Usage: 
                Set settingsAttribute in Bar group
                PMXObjectInstance.setSettingsValue("Bar/settingsAttribute", 10);
                Set settingsAttribute in Global group
                PMXObjectInstance.setSettingsValue("settingsAttribute", 10);
        '''
        value = self.pmxApp.settings.setValue(name, value)
    
    def getSettingsGroup(self, name):
        ''' Shortcut '''
        return self.pmxApp.settings.getGroup(name)
    
    #============================================================
    # Shortcut
    #============================================================
    @property
    def mainWindow(self):
        if self.__class__.__mainwindow == None:
            self.__class__.__mainwindow = self
            while self.__class__.__mainwindow.parent() != None:
                self.__class__.__mainwindow = self.__class__.__mainwindow.parent()
        return self.__class__.__mainwindow
    
    @property
    def pmxApp(self):
        '''
        Shortcut property for PyQt4.QtGui.QApplication.instance().
        '''
        return self.__app

    #============================================================
    # Logger
    #============================================================
    @property
    def logger(self):
        '''
        Per class logger, logger instances are named after
        classes, ie: prymatex.gui.mainwindow.PMXMainWindow 
        '''
        if self.__logger is None:
            t = type(self)
            loggername = '.'.join([t.__module__, t.__name__])
            self.__class__.__logger = getLogger(loggername)
        return self.__logger
    
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg)
    
    def info(self, msg, *args, **kwargs):
        self.logger.info(msg)
    
    def warn(self, msg, *args, **kwargs):
        self.logger.warn(msg)
    
    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg)