#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

from . import types
from .base import compileRegexp

from prymatex.utils import six

# In Snippets

## Placeholders

        # $«int»
        # ${«int»}
        # ${«int»:«snippet»}
        # ${«int»/«regexp»/«format»/«options»}
        # ${«int»|«choice 1»,…,«choice n»|}

## Code

        # `«code»`

# In Format Strings

        # $0-n
        # 
        # \U, \L, \E, \u, \l
        # \t, \r, \n, \x{HHHH}, \xHH
        # 
        # «variables»
        # 
        # (?«var»:«if»:«else»}
        # (?«var»:«if»}

# In Both

## Variables

        # ${«var»:?«if»:«else»}
        # ${«var»:+«if»}
        # ${«var»:-«else»}
        # ${«var»:«else»}
        # ${«var»/«regexp»/«format»/«options»}
        # ${«var»:[/upcase][/downcase][/capitalize][/asciify]}

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
        res.append("")
        while self.it != self.last and self.source[self.it].isdigit():
            res[0] += self.source[self.it]
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
        return False

    def parse_regexp_options(self, options):
        while self.parse_char("giems"):
            options.append(self.source[self.it - 1])
        return True

    def parse_symbol(self, stopChars, nodes):
        backtrack = self.it
        
        while self.it != self.last:
            name = []
            if self.parse_until("/", name):
                res = types.SymbolTransformationType(name.pop())
                regexp = []
                if self.parse_until("/", regexp) and self.parse_format_string("/", res.format) and self.parse_regexp_options(res.options) and (self.parse_char(";") or self.it == self.last):
                    res.pattern = compileRegexp(regexp.pop(), res.options)
                    nodes.append(res)
                    continue
                break
            elif self.parse_text(nodes):
                continue
            break
            
        if (self.it == self.last and len(stopChars) == 0) or self.parse_char(stopChars):
            return True
        self.it = backtrack
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
                if self.source[self.it - 1] == '}':
                    nodes.append(types.VariableType(name.pop()))
                    return True
                elif self.source[self.it - 1] == '/':
                    res = types.VariableTransformationType(name.pop())
                    regexp = []
                    if self.parse_until("/", regexp) and self.parse_format_string("/", res.format) and self.parse_regexp_options(res.options) and self.parse_char("}"):
                        res.pattern = compileRegexp(regexp.pop(), res.options)
                        nodes.append(res)
                        return True
                else: # self.source[self.it - 1] == ':'
                    if self.parse_char("+"):
                        res = types.VariableConditionType(name.pop())
                        if parse_content("}", res.if_set):
                            nodes.append(res)
                            return True
                    elif self.parse_char("?"):
                        res = types.VariableConditionType(name.pop())
                        if parse_content(":", res.if_set) and parse_content("}", res.if_not_set):
                            nodes.append(res)
                            return True
                    elif self.parse_char("/"):
                        res = types.VariableChangeType(name.pop(), types.transform['kNone'] )
                        while self.source[self.it - 1] == '/':
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
                        if self.source[self.it - 1] == '}':
                            nodes.append(res)
                            return True
                    else:
                        self.parse_char("-") # to be backwards compatible, this character is not required
                        res = types.VariableFallbackType( name.pop() )
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
                nodes.append(types.case_change["upper"])
            elif case == 'L':
                nodes.append(types.case_change["lower"])
            elif case == 'E':
                nodes.append(types.case_change["none"])
            elif case == 'u':
                nodes.append(types.case_change["upper_next"])
            elif case == 'l':
                nodes.append(types.case_change["lower_next"])
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
        if not nodes or not isinstance(nodes[-1], types.TextType):
            nodes.append(types.TextType(""))
        nodes[-1].text += char
    
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
                    res = types.PlaceholderChoiceType( index.pop() )
                    while self.parse_format_string(",|", res.choices) and self.source[self.it - 1] == ',':
                        res.choices.append(types.TextType(""))
                    if self.source[self.it - 1] == '|' and self.parse_char("}"):
                        nodes.append(res)
                        return True
                elif self.parse_char("}"):
                    nodes.append(types.PlaceholderType(index.pop()))
                    return True
            elif self.parse_int(index):
                nodes.append(types.PlaceholderType(index.pop()))
                return True
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

def parse_symbol(source):
    nodes = []
    Parser(source).parse_symbol("", nodes)
    return nodes

def parse_format_string(source):
    nodes = []
    Parser(source).parse_format_string("", nodes)
    return nodes

def parse_snippet(source):
    nodes = []
    Parser(source).parse_snippet("", nodes)
    return nodes
