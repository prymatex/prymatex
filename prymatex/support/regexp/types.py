#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import re
from prymatex.utils import six

CASE_UPPER = 0
CASE_LOWER = 1
CASE_NONE = 2
CASE_UPPER_NEXT = 3
CASE_LOWER_NEXT = 4

CASE_CHARS = {
    CASE_UPPER: '\\U',
    CASE_LOWER: '\\L',
    CASE_NONE: '\\E',
    CASE_UPPER_NEXT: '\\u',
    CASE_LOWER_NEXT: '\\l'
}

def escapeCharacters(text, esc):
    for e in esc:
        text = text.replace(e, '\\' + e)            
    return text

class ConditionType(object):
    def __init__(self, name):
        self.name = name
        self.if_set = []
        self.if_not_set = []

    def apply(self, match):
        grps = match.groups()
        index = self.name - 1
        if len(grps) > index and grps[index] is not None:
            return self.if_set
        return self.if_not_set

    def __str__(self):
        cnd = "(?%d:" % self.name
        for cmps in self.if_set:
            if isinstance(cmps, six.integer_types):
                cnd += CASE_CHARS[cmps]
            else:
                cnd += escapeCharacters(six.text_type(cmps), "(:)")
        if self.if_not_set:
            cnd += ":"
            for cmps in self.if_not_set:
                if isinstance(cmps, six.integer_types):
                    cnd += CASE_CHARS[cmps]
                else:
                    cnd += escapeCharacters(six.text_type(cmps), "(:)")
        cnd += ")"
        return cnd
    
    __unicode__ = __str__


class FormatType(object):
    _repl_re = re.compile("\$(?:(\d+)|g<(.+?)>)")
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
        result = []
        match = pattern.search(text)
        if not match: return None
        beginText = text[:match.start()]
        while match:
            nodes = []
            sourceText = text[match.start():match.end()]
            endText = text[match.end():]
            # Translate to conditions
            for composite in self.composites:
                if isinstance(composite, ConditionType):
                    nodes.extend(composite.apply(match))
                else:
                    nodes.append(composite)
            # Transform
            case = CASE_NONE
            for value in nodes:
                if isinstance(value, six.string_types):
                    value = pattern.sub(self.prepare_replacement(value), sourceText)
                elif isinstance(value, six.integer_types):
                    case = value
                    continue
                # Apply case and append to result
                result.append(self.case_function(case)(value))
                if case in [CASE_LOWER_NEXT, CASE_UPPER_NEXT]:
                    case = CASE_NONE
            if 'g' not in flags:
                break
            match = pattern.search(text, match.end())
        return "%s%s%s" % (beginText, "".join(result), endText)

    def __str__(self):
        frmt = ""
        for cmps in self.composites:
            if isinstance(cmps, six.integer_types):
                frmt += CASE_CHARS[cmps]
            else:
                frmt += six.text_type(cmps)
        return frmt
    
    __unicode__ = __str__
        
class TransformationType(object):
    def __init__(self):
        self.pattern = None
        self.format = FormatType()
        self.options = []
        
    def transform(self, text):
        return self.format.apply(self.pattern, text, self.options)

    def __str__(self):
        trns = "%s/%s/" % (self.pattern.pattern, six.text_type(self.format))
        if self.options:
            trns += "%s" % "".join(self.options)
        return trns
    
    __unicode__ = __str__
