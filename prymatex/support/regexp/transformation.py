#!/usr/bin/env python
# encoding: utf-8

from parser import Parser

class Transformation(object):
    def __init__(self, transformation):
        self.transformation = transformation and Parser.transformation(transformation)

    def __str__(self):
        return str(self.transformation)
    
    def __unicode__(self):
        return unicode(self.transformation)
    
    def transform(self, text):
        return self.transformation.transform(text)