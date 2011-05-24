#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import QObject, pyqtWrapperType
import re
from prymatex.core.event import PMXEventSender
from prymatex.core.config import SettingsGroup
from PyQt4.QtGui import qApp
from prymatex.core.exceptions import APIUsageError
METHOD_RE = re.compile('(?P<name>[\w\d_]+)(:?\((?P<args>.*)\))?', re.IGNORECASE)

class InvalidEventSignature(Exception):
    pass

settings = qApp.instance().settings

EVENT_CLASSES = {}

class PMXOptions(object):
    def __init__(self, options):
        self.settings = settings.getGroup(getattr(options, 'settings', ''))
        self.events = getattr(options, 'events', None)

class PMXObjectBase(pyqtWrapperType):
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

class PMXObject(QObject):
    __metaclass__ = PMXObjectBase

    #============================================================
    # Settings
    #============================================================
    def configure(self):
        self._meta.settings.addListener(self)
        self._meta.settings.configure(self)
    
    def __del__(self):
        self._meta.settings.removeListener(self)
    
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
    
    #============================================================
    # Events
    #============================================================
    def declareEvent(self, signature):
        global EVENT_CLASSES
        match = METHOD_RE.match(signature)
        if not match:
                raise InvalidEventSignature(signature)
        name, args = match.group('name'), match.group('args')
        event_class = EVENT_CLASSES.setdefault(name, PMXEventSender.eventFactory(name))
        
        sender = PMXEventSender(event_class = event_class, source = self)
        setattr(self, name, sender)
        return sender

    def connectEventsByName(self):
        raise NotImplementedError("Not implemented error")

    #============================================================
    # Shortcut
    #============================================================
    __mainwindow = None
    @property
    def mainWindow(self):
        if self.__class__.__mainwindow == None:
            self.__class__.__mainwindow = self
            while self.__class__.__mainwindow.parent() != None:
                self.__class__.__mainwindow = self.__class__.__mainwindow.parent()
        return self.__class__.__mainwindow
        
    __app = None
    @property
    def pmxApp(self):
        '''
        Shortcut property for PyQt4.QtGui.QApplication.instance() whit
        slight class level cache.
        '''
        if self.__class__.__app == None:
            from PyQt4.QtGui import QApplication
            self.__class__.__app  = QApplication.instance()
        return self.__class__.__app

    #============================================================
    # Logger
    #============================================================
    __logger = None
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