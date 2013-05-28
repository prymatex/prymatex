#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from prymatex.utils import six

from .parser import Parser

class Transformation(object):
    def __init__(self, transformation):
        self.soruce = transformation
        self.transformation = Parser.transformation(transformation)

    def transform(self, text):
        return self.transformation.transform(text)

    def __str__(self):
        #Por ahora algo de trampa, lo que entra es lo que se ve
        return six.text_type(self.soruce)
    
    __unicode__ = __str__
