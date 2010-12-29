#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
	from PyQt4.QtCore import QEvent
	from PyQt4.Qt import QApplication
	from PyQt4.QtCore import SIGNAL
except:
	#MOCK
	def infinite_generator(initial = 65535):
		while True:
			yield initial
			initial -= 1 

	class QEvent(object):
		generator = infinite_generator()
		
		@classmethod
		def registerEventType(cls):
			return cls.generator.next()

class PMXEvent(QEvent):
	def __init__(self, sender):
		super(PMXEvent, self).__init__(self.TYPE)
		self.sender = sender

class PMXEventSender(object):
	#__metaclass__ = PMXEventBase
	def __init__(self, event_class, sender):
		self.event_class = event_class
		self.sender = sender
		
	def __call__(self, *largs, **kwargs):
		
		event = self.event_class(sender = self.sender)
		QApplication.postEvent(self.sender, event)
		
	@staticmethod
	def eventFactory(name):
		return type(name, (PMXEvent, ), {'TYPE': QEvent.registerEventType(),
										'signal': SIGNAL(name)})
		
def main():
	e1 = type("MyEvent", (PMXEvent, ), {})
	e2 = type("MyOtherEvent", (PMXEvent, ), {})
	print e1.TYPE
	print e2.TYPE
	
if __name__ == "__main__":
	main()