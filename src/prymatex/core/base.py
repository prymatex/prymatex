#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import QObject, pyqtWrapperType
import sip
import re
from prymatex.core.event import PMXEvent, PMXEventSender
from prymatex.config.base import settings
METHOD_RE = re.compile('(?P<name>[\w\d_]+)(:?\((?P<args>.*)\))?', re.IGNORECASE)

class InvalidEventSignature(Exception):
	pass

EVENT_CLASSES = {}

class PMXOptions(object):
    def __init__(self, options=None):
        self.settings = getattr(options, 'settings', None)
        self.events = getattr(options, 'events', None)

class PMXObjectBase(pyqtWrapperType):
    def __new__(cls, name, bases, attrs):
        new_class = super(PMXObjectBase, cls).__new__(cls, name, bases, attrs)
        opts = new_class._meta = PMXOptions(getattr(new_class, 'Meta', None))
        if opts.settings:
            sns = settings
            for base in bases:
                if hasattr(base, '_meta') and hasattr(base._meta, 'settings') and base._meta.settings != None:
                    sns = getattr(sns, base._meta.settings[0])
            class_settings = sns.setdefault(*opts.settings)
            class_settings.add_to_class(new_class)
        return new_class

class PMXObject(QObject):
    __metaclass__ = PMXObjectBase
    
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