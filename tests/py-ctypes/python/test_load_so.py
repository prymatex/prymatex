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

class Point(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float)]

Point_p = POINTER(Point)
p1, p2 = Point(2, 4.3), Point(20.17, 55.89)
    
print Point_p
lib.distancia.restype = c_float
lib.distancia.argtypes = [Point_p, Point_p]
print "Ejecutando"
print lib.distancia(p1, p2)