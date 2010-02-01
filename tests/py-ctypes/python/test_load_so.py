#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 01/02/2010 by defo

from ctypes import *

LIB_PATH = '../C/libmylib.so'

lib = cdll.LoadLibrary(LIB_PATH)
print "Vamos a probar si le podemos pedir una cadena a la librería"
print lib.say_hello()
print "Nos dio un puntero hexa %8x" % lib.say_hello()

print "Ahora definimos que la salida es char* (en ctypes c_char_p)"
lib.say_hello.restype = c_char_p
print "Y la llamamamos: ", lib.say_hello()

