#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from . import types
from .base import compileRegexp

from prymatex.utils import six

class Parser(object):
    def __init__(self, source):
        self.source = source
        self.it = 0
        self.last = len(source)
    
    def parse_char(self, ch):
        if self.it != self.last:
            if self.source[self.it] in ch:
                self.it += 1
                return True
        return False

    def parse_chars(self, chars, res):
        chs = ""
        while(self.it != self.last and self.source[self.it] in chars):
            chs += self.source[self.it]
            self.it += 1
        if chs:
            res.append(chs)
        return bool(res)

    def parse_int(self, res):
        if self.it == self.last or not self.source[self.it].isdigit():
            return False
        res.append(0)
        while self.it != self.last and self.source[self.it].isdigit():
            res[0] = (res[0] * 10) + int(self.source[self.it])
            self.it += 1
        return True

    def parse_until(self, stopChars, res):
        chrs = ""
        backtrack = self.it
        while self.it != self.last and self.source[self.it] not in stopChars:
            if self.source[self.it] == '\\' \
                and self.it + 1 != self.last \
                and (self.source[self.it + 1] == '\\' \
                    or self.source[self.it + 1] in stopChars):
                self.it += 1
            chrs += self.source[self.it];
            self.it += 1
        if self.parse_char(stopChars):
            res.append(chrs)
            return True
        self.it = backtrack
        return false

    def parse_regexp_options(self, options):
        while self.parse_char("giems"):
            options.append(self.source[self.it - 1])
        return True

    def parse_transformation(self, nodes):
        res = types.VariableTransformationType("none")
        regexp = []
        if self.parse_until("/", regexp) \
            and self.parse_format_string("/", res.format.composites) \
            and self.parse_regexp_options(res.options):
            res.pattern = compileRegexp(regexp.pop(), res.options)
            nodes.append(res)
            return True
        return False

    def parse_format_string(self, stopChars, nodes):
        backtrack = self.it
        esc = "\\$(" + stopChars

        while self.it != self.last and self.source[self.it] not in stopChars:
            if False or self.parse_variable(self.parse_format_string, nodes) \
                or self.parse_condition(nodes) \
                or self.parse_control_code(nodes) \
                or self.parse_case_change(nodes) \
                or self.parse_escape(esc, nodes) \
                or self.parse_text(nodes):
                continue
            break

        if (self.it == self.last and len(stopChars) == 0) or self.parse_char(stopChars):
            return True
        self.it = backtrack
        return False

    def parse_variable(self, parse_content, nodes):
        backtrack = self.it
        if self.parse_char("$"):
            name = []
            if self.parse_char("{") and self.parse_until("/:}", name):
                if self.it[-1] == '}':
                    nodes.append(types.VariableType(name.pop()))
                    return True
                elif self.it[-1] == '/':
                    res = types.VariableTransformationType(name.pop())
                    regexp = []
                    if self.parse_until("/", regexp) and self.parse_format_string("/", res.format) and self.parse_regexp_options(res.options) and parse_char("}"):
                        res.pattern = compileRegexp(regexp.pop(), res.options)
                        nodes.append(res)
                        return True
                else: # it[-1] == ':'
                    if self.parse_char("+"):
                        res = types.VariableConditionType(name.pop())
                        if parse_content("}", res.if_set):
                            nodes.append(res)
                            return True
                    elif self.parse_char("?"):
                        res = types.VariableConditionType(name)
                        if parse_content(":", res.if_set) and parse_content("}", res.if_not_set):
                            nodes.append(res)
                            return True
                    elif self.parse_char("/"):
                        res = types.VariableChangeType(name, types.transform['kNone'] )
                        while self.it[-1] == '/':
                            option = []
                            if self.parse_until("/}", option):
                                option = option.pop()
                                res.change |= { 
                                    "upcase": types.transform['kUpcase'],
                                    "downcase": types.transform['kDowncase'],
                                    "capitalize": types.transform['kCapitalize'],
                                    "asciify": types.transform['kAsciify'] }[option]
                            else:
                                break                                
                        if self.it[-1] == '}':
                            nodes.append(res)
                            return True
                    else:
                        self.parse_char("-") # to be backwards compatible, this character is not required
                        res = types.VariableFallbackType( name )
                        if parse_content("}", res.fallback):
                            nodes.append(res)
                            return True
            else:
                index = []
                if self.parse_int(index):
                    nodes.append(types.VariableType(index.pop()))
                    return True
                variable = []
                if self.parse_chars("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_abcdefghijklmnopqrstuvwxyz", variable):
                    nodes.append(types.VariableType(variable.pop()))
                    return True
        self.it = backtrack
        return False

    def parse_condition(self, nodes):
        backtrack = self.it
        captureRegister = []
        if self.parse_char("(") and self.parse_char("?") and self.parse_int(captureRegister) and self.parse_char(":"):
            res = types.VariableConditionType(captureRegister.pop())
            if self.parse_format_string(":)", res.if_set) \
                and (self.source[self.it - 1] == ')' or \
                    self.source[self.it - 1] == ':' and \
                    self.parse_format_string(")", res.if_not_set) \
                and self.source[self.it - 1] == ')'):
                nodes.append(res)
                return True
        self.it = backtrack
        return False

    def parse_control_code(self, nodes):
        backtrack = self.it
        if self.parse_char("\\") and self.parse_char("trn"):
            code = self.source[self.it - 1]
            if code == 't':
                self.text_node(nodes, '\t')
            elif code == 'r':
                self.text_node(nodes, '\r')
            elif code == 'n': 
                self.text_node(nodes, '\n')
            return True
        self.it = backtrack
        return False
        
    def parse_case_change(self, nodes):
        backtrack = self.it
        if(self.parse_char("\\") and self.parse_char("ULEul")):
            case = self.source[self.it - 1]
            if case == 'U':
                nodes.append(types.CASE_UPPER)
            elif case == 'L':
                nodes.append(types.CASE_LOWER)
            elif case == 'E':
                nodes.append(types.CASE_NONE)
            elif case == 'u':
                nodes.append(types.CASE_UPPER_NEXT)
            elif case == 'l':
                nodes.append(types.CASE_LOWER_NEXT)
            return True
        self.it = backtrack
        return False
        
    def parse_escape(self, esc, nodes):
        backtrack = self.it
        if self.parse_char("\\") and self.parse_char(esc):
            self.text_node(nodes, self.source[self.it -1])
            return True
        self.it = backtrack;
        return False

    def parse_text(self, nodes):
        if self.it != self.last:
            self.text_node(nodes, self.source[self.it])
            self.it += 1
            return True
        return False

    def text_node(self, nodes, char):
        if not nodes or not isinstance(nodes[-1], six.string_types):
            nodes.append("")
        nodes[-1] = nodes[-1] + char
    
    def parse_placeholder(self, nodes):
        backtrack = self.it
        if self.parse_char("$"):
            index = []
            if self.parse_char("{") and self.parse_int(index):
                if self.parse_char(":"):
                    res = types.PlaceholderType(index.pop())
                    if self.parse_snippet("}", res.content):
                        nodes.append(res)
                        return True
                    elif self.parse_char("/"):
                        regexp = []
                        res = types.PlaceholderTransformType( index.pop() )
                        if self.parse_until("/", regexp) and self.parse_format_string("/", res.format) and self.parse_regexp_options(res.options) and self.parse_char("}"):
                            res.pattern = compileRegexp(regexp.pop(), res.options)
                            nodes.append(res)
                            return True
                    elif self.parse_char("|"):
                        res = PlaceholderChoiceType( index.pop() )
                        while self.parse_format_string(",|", res.choices) and self.it[-1] == ',':
                            pass
                        if self.it[-1] == '|' and self.parse_char("}"):
                            nodes.append(res)
                            return True
                    elif self.parse_char("}"):
                        nodes.append(types.PlaceholderType(index.pop()))
                        return True
            elif self.parse_int(index):
                nodes.append(types.PlaceholderType(index.pop()))
                return True;
        self.it = backtrack
        return False

    def parse_code(self, nodes):
        backtrack = self.it
        code = []
        if self.parse_char("`") and self.parse_until("`", code):
            nodes.append(types.CodeType(code.pop()))            
            return True
        self.it = backtrack
        return False
    
    def parse_snippet(self, stopChars, nodes):
        backtrack = self.it
        esc = "\\$`" + stopChars

        while self.it != self.last and self.source[self.it] not in stopChars:
            if False or self.parse_placeholder(nodes) \
                or self.parse_variable(self.parse_snippet, nodes) \
                or self.parse_code(nodes) \
                or self.parse_escape(esc, nodes) \
                or self.parse_text(nodes):
                continue
            break

        if (self.it == self.last and len(stopChars) == 0) or self.parse_char(stopChars):
            return True
        self.it = backtrack
        return False
    
    # = API =
    @staticmethod
    def format(source):
        frmt = types.FormatType()
        if Parser(source).parse_format_string("", frmt.composites):
            return frmt
    
    @staticmethod
    def transformation(source):
        nodes = []
        if Parser(source).parse_transformation(nodes):
            return nodes.pop()

def parse_format_string(source):
    nodes = []
    Parser(source).parse_format_string("", nodes)
    return nodes

def parse_snippet(source):
    nodes = []
    Parser(source).parse_snippet("", nodes)
    return nodes
