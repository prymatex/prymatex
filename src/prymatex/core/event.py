#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
	from PyQt4.QtCore import QEvent, QObject
	from PyQt4.Qt import QApplication, QAction
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
	def __init__(self, source, largs, kwargs):
		super(PMXEvent, self).__init__(self.TYPE)
		self.source = source
		self.largs, self.kwargs = largs, kwargs

class PMXEventSender(QObject):
	'''
	Sends an event whenever it's called, it should be attached
	to a QObject.
	'''
	#__metaclass__ = PMXEventBase
	def __init__(self, event_class, source, action = None):
		self.event_class = event_class
		self.source = source
		if action:
			assert isinstance(action, QAction)
			self.connect(action, SIGNAL('triggered()'), self)
		
	def __call__(self, *largs, **kwargs):
		
		event = self.event_class(source = self.source, 
								largs = largs,
								kwargs = kwargs)
		QApplication.postEvent(self.source, event)
		
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