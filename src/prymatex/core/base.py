#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import QObject, SIGNAL
from PyQt4.QtGui import QAction
import re
from prymatex.core.event import PMXEvent, PMXEventSender
import inspect

from logging import getLogger
logger = getLogger(__name__)

METHOD_RE = re.compile(r'(?P<name>[\w\d_]+)(:?\((?P<args>.*)\))?', re.IGNORECASE)
EVENT_HANDLER_RE = re.compile(r'^on_(?P<name>[\w\d\_]+)')

def is_event_handler(method_name):
	return EVENT_HANDLER_RE.match(method_name) != None

def event_signal_name(method_name):
	return EVENT_HANDLER_RE.match(method_name).group('name')
	
class InvalidEventSignature(Exception):
	pass


EVENT_CLASSES = {}

class PMXObject(QObject):
	
	def declareEvent(self, signature):
		global EVENT_CLASSES
		match = METHOD_RE.match(signature)
		if not match:
			raise InvalidEventSignature(signature)
		name, args = match.group('name'), match.group('args')
		event_class = EVENT_CLASSES.setdefault(name, 
											PMXEventSender.eventFactory(name))
		
		sender = PMXEventSender(event_class = event_class, source = self)
		setattr(self, name, sender)
		return sender

	def connectEventsByName(self):
		'''
		Connects signal with events matching with the signature
		on_<signal_name> where signal name ends in Event
		'''
		
		names = filter(is_event_handler, dir(self))
		#print "*** Names are: %s for %s" % (names, self)
		for name in names:
			callback = getattr(self, name)
			if inspect.ismethod(callback):
				signal = event_signal_name(name) + '()'
				self.connect(self.root, SIGNAL(signal), callback)
				logger.debug("Coneccting %s with %s", name, callback)
				print "*** Connect"
			else:
				logger.warning("Could not connect %s", name)
			
	
	def declarActionsAsEvents(self, *action_names):
		for name in action_names:
			action = getattr(self, name, None)
			if not action:
				logger.warning("Could not find action %s in %s", name, self)
		
	
	def declareActionEvent(self, action):
		'''
		Generates an event when an action is triggered
		'''
		assert isinstance(action, QAction), "%s is not a QAction instance" % action
		event_sender = self.declareEvent(signature)
	
	@property
	def root(self):
		root = self
		while root.parent():
			root = root.parent()
		return root