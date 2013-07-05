#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import re
from prymatex.utils import six

regexp_options = { 
    'none': 1 << 0,
    'g': 1 << 1,
    'i': 1 << 2,
    'e': 1 << 3,
    'm': 1 << 4,
    's': 1 << 5 }

case_change = { 
    'none': 0, 
    'upper_next': 1,
    'lower_next': 2,
    'upper': 3, 
    'lower': 4 }

transform = { 
    'kNone': 0 << 0, 
    'kUpcase': 1 << 0,
    'kDowncase': 1 << 1,
    'kCapitalize': 1 << 2, 
    'kAsciify': 1 << 3 }

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

#struct variable_t { std::string name; WATCH_LEAKS(parser::variable_t); };
class VariableType(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "$" + six.text_type(self.name)
    
    __unicode__ = __str__

#struct variable_condition_t { std::string name; nodes_t if_set, if_not_set; WATCH_LEAKS(parser::variable_condition_t); };
class VariableConditionType(object):
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

# TODO: Quitar este
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
                if isinstance(composite, VariableConditionType):
                    nodes.extend(composite.apply(match))
                else:
                    nodes.append(composite)
            # Transform
            case = CASE_NONE
            for value in nodes:
                if isinstance(value, six.string_types):
                    value = pattern.sub(self.prepare_replacement(value), sourceText)
                elif isinstance(value, VariableType):
                    value = match.groups()[value.name - 1]
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
        try:
            result = "%s%s%s" % (beginText, "".join(result), endText)
        except Exception as ex:
            print(ex, result, six.text_type(self))
        return result 

    def __str__(self):
        frmt = ""
        for cmps in self.composites:
            if isinstance(cmps, six.integer_types):
                frmt += CASE_CHARS[cmps]
            else:
                frmt += six.text_type(cmps)
        return frmt
    
    __unicode__ = __str__

#struct text_t { std::string text; WATCH_LEAKS(parser::text); };
class TextType(object):
    def __init__(self, text):
        self.text = text

#struct placeholder_t { size_t index; nodes_t content; WATCH_LEAKS(parser::placeholder_t); };
class PlaceholderType(object):
    def __init__(self, index):
        self.index = index
        self.content = []
        
#struct placeholder_choice_t { size_t index; std::vector<nodes_t> choices; WATCH_LEAKS(parser::placeholder_choice_t); };
class PlaceholderChoiceType(object):
    def __init__(self, index):
        self.index = index
        self.choices = []

#struct placeholder_transform_t { size_t index; regexp::pattern_t pattern; nodes_t format; regexp_options::type options; WATCH_LEAKS(parser::placeholder_transform_t); };
class PlaceholderTransformType(object):
    def __init__(self, index):
        self.index = index
        self.pattern = None
        self.format = []
        self.options = regexp_options['none']

#struct variable_fallback_t { std::string name; nodes_t fallback; WATCH_LEAKS(parser::variable_fallback_t); };
class VariableFallbackType(object):
    def __init__(self, name, change):
        self.name = name
        self.fallback = []
        
#struct variable_change_t { std::string name; uint8_t change; WATCH_LEAKS(parser::variable_change_t); };
class VariableChangeType(object):
    def __init__(self, name, change):
        self.name = name
        self.change = change
        
#struct variable_transform_t { std::string name; regexp::pattern_t pattern; nodes_t format; regexp_options::type options; WATCH_LEAKS(parser::variable_transform_t); };
class VariableTransformationType(object):
    def __init__(self, name):
        self.name = name
        self.pattern = None
        # TODO: Sacar este format se tiene que resolver aca
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

#struct code_t { std::string code; WATCH_LEAKS(parser::code_t); };
class CodeType(object):
    def __init__(self, code):
        self.code = code
