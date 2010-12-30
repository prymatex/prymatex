#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import QObject
import re
from prymatex.core.event import PMXEvent, PMXEventSender
METHOD_RE = re.compile('(?P<name>[\w\d_]+)(:?\((?P<args>.*)\))?', re.IGNORECASE)

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
		pass
	
	@property
	def root(self):
		root = self
		while root.parent():
			root = root.parent()
		return root