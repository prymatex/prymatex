#!/usr/bin/env python
# encoding: utf-8

import re

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

    def apply(self, match):
        return len(match.groups()) >= self.name and self.if_set or self.if_not_set

class FormatType(object):
    _repl_re = re.compile(u"\$(?:(\d+)|g<(.+?)>)")
    def __init__(self):
        self.composites = []
    
    def case_function(self, case):
        return {
            CASE_UPPER: lambda x : x.upper(),
            CASE_LOWER: lambda x : x.lower(),
            CASE_NONE: lambda x : x,
            CASE_UPPER_NEXT: lambda x : x[0].upper() + x[1:],
            CASE_LOWER_NEXT: lambda x : x[0].lower() + x[1:],
        }[case]
        
    @staticmethod
    def prepare_replacement(text):
        def expand(m, template):
            def handle(match):
                numeric, named = match.groups()
                if numeric:
                    return m.group(int(numeric)) or ""
                return m.group(named) or ""
            return FormatType._repl_re.sub(handle, template)
        if '$' in text:
            return lambda m, r = text: expand(m, r)
        else:
            return lambda m, r = text: r

    def apply(self, pattern, text, flags):
        print flags
        nodes = []
        match = pattern.search(text) if 'g' in flags else pattern.match(text)
        if match:
            for composite in self.composites:
                if isinstance(composite, ConditionType):
                    nodes.extend(composite.apply(match))
                else:
                    nodes.append(composite)
        result = []
        case = CASE_NONE
        for value in nodes:
            if isinstance(value, basestring):
                value = pattern.sub(self.prepare_replacement(value), text)
            elif isinstance(value, int):
                case = value
                continue
            result.append(self.case_function(case)(value))
            if case in [CASE_LOWER_NEXT, CASE_UPPER_NEXT]:
                case = CASE_NONE
        return "".join(result)