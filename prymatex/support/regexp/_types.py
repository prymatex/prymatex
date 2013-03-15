#!/usr/bin/env python
# encoding: utf-8

CASE_UPPER = 0
CASE_LOWER = 1
CASE_NONE = 2
CASE_UPPER_NEXT = 3
CASE_LOWER_NEXT = 4

class ConditionType(object):
    def __init__(self, name):
        self.name = name
        self.if_set = []
        self.if_not_set = []

class FormatType(object):
    def __init__(self):
        self.composites = []
        