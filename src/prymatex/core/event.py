#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
	from PyQt4.QtCore import QEvent
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

class PMXEventBase(type):
	def __new__(cls, name, bases, attrs):
		new_class = super(PMXEventBase, cls).__new__(cls, name, bases, attrs)
		setattr(new_class, "TYPE", QEvent.registerEventType())
		return new_class

class PMXEvent(QEvent):
	__metaclass__ = PMXEventBase

	def post(self):
		pass
	
def main():
	e1 = type("MyEvent", (PMXEvent, ), {})
	e2 = type("MyOtherEvent", (PMXEvent, ), {})
	print e1.TYPE
	print e2.TYPE
	
if __name__ == "__main__":
	main()