#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import QObject, pyqtWrapperType
import re
from prymatex.core.event import PMXEventSender
from PyQt4.QtGui import qApp
METHOD_RE = re.compile('(?P<name>[\w\d_]+)(:?\((?P<args>.*)\))?', re.IGNORECASE)

class InvalidEventSignature(Exception):
	pass

settings = qApp.instance().settings

EVENT_CLASSES = {}

class PMXOptions(object):
    def __init__(self, options=None):
        self.settings = settings
        space = getattr(options, 'settings', None)
        if space != None:
            spaces = space.split('.')
            for s in spaces:
                self.settings = getattr(self.settings, s)
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

    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)

class PMXObject(QObject):
    __metaclass__ = PMXObjectBase

    def configure(self):
        self._meta.settings.add_listener(self)
        self._meta.settings.configure(self)
    
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
        pass
    
    @property
    def root(self):
        root = self
        while root.parent():
            root = root.parent()
        return root