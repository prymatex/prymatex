#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class PMXObjectBase(QtCore.pyqtWrapperType):
    def __new__(cls, name, bases, attrs):
        module, settings = attrs.pop('__module__'), attrs.pop('SETTINGS_GROUP', name)
        
        #Build class
        new_class = super(PMXObjectBase, cls).__new__(cls, name, bases, { '__module__': module })
        
        #Settings for class
        settings = QtGui.QApplication.instance().settings.getGroup(settings)
        new_class.add_to_class('settings', settings)
        
        #Other attrs
        for name, attr in attrs.iteritems():
            new_class.add_to_class(name, attr)
        return new_class

    def add_to_class(cls, name, value): #@NoSelf
        if hasattr(value, 'contributeToClass'):
            value.contributeToClass(cls, name)
        else:
            setattr(cls, name, value)

class PMXObject(QtCore.QObject):
    __metaclass__ = PMXObjectBase
    __app = QtGui.QApplication.instance()
    __mainwindow = None
    __logger = None
    
    def __del__(self):
        self.settings.removeListener(self)
        
    #============================================================
    # Settings
    #============================================================
    def configure(self):
        self.settings.addListener(self)
        self.settings.configure(self)
    
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
    def application(self):
        """
        Shortcut property for PyQt4.QtGui.QApplication.instance().
        """
        return self.__app

    #============================================================
    # Logger
    #============================================================
    @property
    def logger(self):
        """
        Per class logger, logger instances are named after
        classes, ie: prymatex.gui.mainwindow.PMXMainWindow 
        """
        from logging import getLogger
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
