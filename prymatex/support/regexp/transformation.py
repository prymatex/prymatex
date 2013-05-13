#!/usr/bin/env python
# encoding: utf-8

from .parser import Parser

class Transformation(object):
    def __init__(self, transformation):
        self.soruce = transformation
        self.transformation = Parser.transformation(transformation)

    def __str__(self):
        #Por ahora algo de trampa, lo que entra es lo que se ve
        return str(self.soruce)
    
    def __unicode__(self):
        #Por ahora algo de trampa, lo que entra es lo que se ve
        return str(self.soruce)
    
    def transform(self, text):
        return self.transformation.transform(text)