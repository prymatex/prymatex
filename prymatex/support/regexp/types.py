#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from collections import namedtuple

import re
from prymatex.utils import six
from prymatex.utils import text

case_change = { 
    'none': 0, 
    'upper_next': 1,
    'lower_next': 2,
    'upper': 3, 
    'lower': 4 }

case_chars = {
    case_change['none']: '\\E',
    case_change['upper_next']: '\\u',
    case_change['lower_next']: '\\l',
    case_change['upper']: '\\U',
    case_change['lower']: '\\L',
}

case_function = {
    case_change['none']: lambda x : x,
    case_change['upper_next']: lambda x : x[0].upper() + x[1:],
    case_change['lower_next']: lambda x : x[0].lower() + x[1:],
    case_change['upper']: lambda x : x.upper(),
    case_change['lower']: lambda x : x.lower(),
}

transform = { 
    'kNone': 0 << 0, 
    'kUpcase': 1 << 0,
    'kDowncase': 1 << 1,
    'kCapitalize': 1 << 2, 
    'kAsciify': 1 << 3 
}

transform_function = {
    transform['kNone']: lambda x : x,
    transform['kUpcase']: lambda x : x.upper(),
    transform['kDowncase']: lambda x : x.lower(),
    transform['kCapitalize']: lambda x : x.title(),
    transform['kAsciify']: text.asciify,
}

Memo = namedtuple("Memo", "identifier start end content")

class Memodict(dict):
    def create_identifier(self, obj):
        return id(obj)

    def get_or_create(self, obj):
        identifier = self.create_identifier(obj)
        if identifier in self:
            return self[identifier]
        return self.setdefault(identifier, obj.memoFactory(identifier))
    
    def set(self, obj, memo):
        identifier = self.create_identifier(obj)
        self[identifier] = memo

def escapeCharacters(text, esc):
    for e in esc:
        text = text.replace(e, '\\' + e)            
    return text

#struct variable_t { std::string name; WATCH_LEAKS(parser::variable_t); };
class VariableType(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        if self.name.isdigit():
            return "$%s" % self.name
        else:
            return "${%s}" % self.name

    def replace(self, memodict, holders = None, match = None, variables = None):
        if match and self.name.isdigit():
            try:
                return match.group(int(self.name))
            except:
                pass
        return variables.get(self.name, "")

    def render(self, visitor, memodict, holders = None, match = None):
        visitor.insertText(self.replace(memodict, holders, match, visitor.environmentVariables()))

#struct variable_condition_t { std::string name; nodes_t if_set, if_not_set; WATCH_LEAKS(parser::variable_condition_t); };
class VariableConditionType(object):
    def __init__(self, name):
        self.name = name
        self.if_set = []
        self.if_not_set = []

    def __str__(self):
        cnd = "(?%s:" % self.name
        for cmps in self.if_set:
            if isinstance(cmps, six.integer_types):
                cnd += case_chars[cmps]
            else:
                cnd += escapeCharacters(six.text_type(cmps), "(:)")
        if self.if_not_set:
            cnd += ":"
            for cmps in self.if_not_set:
                if isinstance(cmps, six.integer_types):
                    cnd += case_chars[cmps]
                else:
                    cnd += escapeCharacters(six.text_type(cmps), "(:)")
        cnd += ")"
        return cnd
    
    def replace(self, memodict, holders = None, match = None, variables = None):
        group = match.group(int(self.name))
        nodes = self.if_set if group else self.if_not_set
        text = ""
        case = case_change['none']
        for node in nodes:
            if isinstance(node, six.integer_types):
                case = node
                continue
            value = node.replace(memodict, holders, match, variables)
            # Apply case and append to result
            text += case_function[case](value)
            if case in [case_change['upper_next'], case_change['lower_next']]:
                case = case_change['none']
        return text

    def render(self, visitor, memodict, holders = None, match = None):
        visitor.insertText(self.replace(memodict, holders, match, visitor.environmentVariables()))

#struct text_t { std::string text; WATCH_LEAKS(parser::text); };
class TextType(object):
    def __init__(self, text):
        self.text = text
    
    def __str__(self):
        return "%s" % self.text
    
    def replace(self, memodict, holders = None, match = None, variables = None):
        return self.text

    def render(self, visitor, memodict, holders = None, match = None):
        visitor.insertText(self.replace(memodict, holders, match, visitor.environmentVariables()))

class PlaceholderTypeMixin(object):
    def memoFactory(self, identifier):
        raise NotImplemented

    def hasContent(self, memodict):
        return memodict.get_or_create(self).content is not None
        
    def setContent(self, text, memodict):
        memodict.set(self, memodict.get_or_create(self)._replace(content=text))
        return True
    
    def getContent(self, memodict):
        return memodict.get_or_create(self).content

    def position(self, memodict):
        memo = memodict.get_or_create(self)
        return memo.start, memo.end

#struct placeholder_t { size_t index; nodes_t content; WATCH_LEAKS(parser::placeholder_t); };
class PlaceholderType(PlaceholderTypeMixin):
    def __init__(self, index):
        self.index = index
        self.content = []
    
    def __str__(self):
        if self.content:
            return "${%s:%s}" % (self.index, "".join(["%s" % node for node in self.content]))
        else:
            return "$%s" % self.index

    def collect(self, other, chain):
        if other == self:
            return True
        elif self.content:
            for node in self.content:
                if isinstance(node, PlaceholderType):
                    if node.collect(other, chain):
                        chain.append(self)
                        return True
        else:
            return False
        
    def replace(self, memodict, holders = None, match = None, variables = None):
        memo = memodict.get_or_create(self)
        if memo.content is not None:
            return memo.content
        elif holders[self.index] != self:
            #Mirror
            return holders[self.index].replace(memodict, holders, match, variables)
        else:
            return "".join([node.replace(memodict, holders, match, variables)
                for node in self.content ])
    
    def render(self, visitor, memodict, holders=None, match=None):
        memo = memodict.get_or_create(self)
        start = visitor.caretPosition()
        
        if memo.content is not None:
            visitor.insertText(memo.content)
        elif holders[self.index] != self:
            #Mirror
            visitor.insertText(holders[self.index].replace(memodict, holders, match, visitor.environmentVariables()))
        else:
            for node in self.content:
                node.render(visitor, memodict, holders, match)

        end = visitor.caretPosition()
        memodict.set(self, memo._replace(start=start, end=end))
    
    def hasContent(self, memodict):
        return PlaceholderTypeMixin.hasContent(self, memodict) or bool(self.content)
    
    def memoFactory(self, identifier):
        return Memo(identifier=identifier, start=0, end=0, content=None)
        
#struct placeholder_choice_t { size_t index; std::vector<nodes_t> choices; WATCH_LEAKS(parser::placeholder_choice_t); };
class PlaceholderChoiceType(PlaceholderTypeMixin):
    def __init__(self, index):
        self.index = index
        self.choices = []

    def __str__(self):
        return "${%s|%s|}" % (self.index, ",".join([ "%s" % choice for choice in self.choices]))

    def replace(self, memodict, holders = None, match = None, variables = None):
        memo = memodict.get_or_create(self)
        if isinstance(memo.content, int):
            return self.choices[memo.content].replace(memodict, holders, match, variables)
        return memo.content

    def render(self, visitor, memodict, holders = None, match = None):
        memo = memodict.get_or_create(self)
        start = visitor.caretPosition()
        
        visitor.insertText(self.replace(memodict, holders, match, visitor.environmentVariables()))

        end = visitor.caretPosition()
        memodict.set(self, memo._replace(start = start, end = end))
    
    def hasContent(self, memodict):
        return PlaceholderTypeMixin.hasContent(self, memodict) or bool(self.choices)
    
    def memoFactory(self, identifier):
        return Memo(identifier=identifier, start=0, end=0, content=0)
        
#struct placeholder_transform_t { size_t index; regexp::pattern_t pattern; nodes_t format; regexp_options::type options; WATCH_LEAKS(parser::placeholder_transform_t); };
class PlaceholderTransformType(PlaceholderTypeMixin):
    def __init__(self, index):
        self.index = index
        self.pattern = None
        self.format = []
        self.options = []

    def __str__(self):
        return "${%s/%s/%s/%s}" % (self.index, 
            escapeCharacters(self.pattern.pattern, "/"), 
            "".join([ "%s" % frmt for frmt in self.format]),
            "".join(self.options))
    
    def replace(self, memodict, holders=None, match=None, variables=None):
        text = ""
        value = holders[self.index].replace(memodict, holders, match, variables)
        match = self.pattern.search(value)
        index = 0
        while match:
            if self.format:
                text += value[index:match.start()] + "".join([ frmt.replace(memodict, holders, match, variables) for frmt in self.format])
            else:
                text += value[index:match.start()]
            index = match.end()
            if 'g' not in self.options:
                break
            match = self.pattern.search(value, match.end())
        return text + value[index:]

    def render(self, visitor, memodict, holders = None, match = None):
        memo = memodict.get_or_create(self)
        start = visitor.caretPosition()
        
        visitor.insertText(self.replace(memodict, holders, match, visitor.environmentVariables()))
        
        end = visitor.caretPosition()
        memodict.set(self, memo._replace(start = start, end = end))

    def hasContent(self, memodict):
        return PlaceholderTypeMixin.hasContent(self, memodict) or True

    def memoFactory(self, identifier):
        return Memo(identifier=identifier, start=0, end=0, content=None)
        
#struct variable_fallback_t { std::string name; nodes_t fallback; WATCH_LEAKS(parser::variable_fallback_t); };
class VariableFallbackType(object):
    def __init__(self, name):
        self.name = name
        self.fallback = []
    
    def replace(self, memodict, holders = None, match = None, variables = None):
        if self.name in variables:
            return variables[self.name]
        return "".join([ "%s" % node for node in self.fallback ])
        
    def render(self, visitor, memodict, holders = None, match = None):
        visitor.insertText(self.replace(memodict, holders, match, visitor.environmentVariables()))

#struct variable_change_t { std::string name; uint8_t change; WATCH_LEAKS(parser::variable_change_t); };
class VariableChangeType(object):
    def __init__(self, name, change):
        self.name = name
        self.change = change

    def __str__(self):
        changes = [""]
        return "${%s:%s}" % (self.name, "/".join(changes))
    
    def replace(self, memodict, holders = None, match = None, variables = None):
        text = match.group(int(self.name))
        for key, function in transform_function.items():
            if self.change & key:
                text = function(text)
        return text
        
    def render(self, visitor, memodict, holders = None, match = None):
        visitor.insertText(self.replace(memodict, holders, match, visitor.environmentVariables()))

#struct variable_transform_t { std::string name; regexp::pattern_t pattern; nodes_t format; regexp_options::type options; WATCH_LEAKS(parser::variable_transform_t); };
class VariableTransformationType(object):
    def __init__(self, name):
        self.name = name
        self.pattern = None
        self.format = []
        self.options = []
    
    def __str__(self):
        return "${%s/%s/%s/%s}" % (self.name, 
            escapeCharacters(self.pattern.pattern, "/"),
            "".join([ "%s" % frmt for frmt in self.format]),
            "".join(self.options))
    
    def replace(self, memodict, holders = None, match = None, variables = None):
        if holders and self.name in holders:
            value = holders[self.name].replace(memodict, holders, match, variables)
        elif match and self.name.isdigit():
            value = match.group(int(self.name))
        else:
            value = variables.get(self.name, "")
        text = ""
        match = self.pattern.search(value)
        while match:
            case = case_change['none']
            for frmt in self.format:
                if isinstance(frmt, six.integer_types):
                    case = frmt
                    continue
                value = frmt.replace(memodict, holders, match, variables)
                # Apply case and append to result
                text += case_function[case](value)
                if case in [case_change['upper_next'], case_change['lower_next']]:
                    case = case_change['none']
            if 'g' not in self.options:
                break
            match = self.pattern.search(value, match.end())
        return text

    def render(self, visitor, memodict, holders = None, match = None):
        visitor.insertText(self.replace(memodict, holders, match, visitor.environmentVariables()))
        
#struct variable_transform_t { std::string name; regexp::pattern_t pattern; nodes_t format; regexp_options::type options; WATCH_LEAKS(parser::variable_transform_t); };
class SymbolTransformationType(VariableTransformationType):
    def __str__(self):
        return "%s/%s/%s/%s" % (self.name, 
            escapeCharacters(self.pattern.pattern, "/"),
            "".join([ "%s" % frmt for frmt in self.format]),
            "".join(self.options))

#struct code_t { std::string code; WATCH_LEAKS(parser::code_t); };
class CodeType(object):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return "`%s`" % (self.code)
    
    def replace(self, memodict, holders = None, match = None, variables = None):
        memo = memodict.get_or_create(self)
        if memo.content is not None:
            return memo.content

    def render(self, visitor, memodict, holders = None, match = None):
        memo = memodict.get_or_create(self)
        if memo.content is None:
            memodict.set(self, memo._replace(content = visitor.runShellScript(self.code)))
        visitor.insertText(self.replace(memodict, holders, match, visitor.environmentVariables()))
    
    def memoFactory(self, identifier):
        return Memo(identifier=identifier, start=0, end=0, content=None)
