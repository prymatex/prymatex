#!/usr/bin/env python
# encoding: utf-8

import types
from base import compileRegexp

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
        if(self.it == self.last or not self.source[self.it].isdigit()):
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
        res = types.TransformationType()
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
            if False or self.parse_condition(nodes) \
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

    def parse_condition(self, nodes):
        backtrack = self.it
        captureRegister = []
        if self.parse_char("(") and self.parse_char("?") and self.parse_int(captureRegister) and self.parse_char(":"):
            res = types.ConditionType(captureRegister.pop())
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
        if not nodes or not isinstance(nodes[-1], basestring):
            nodes.append("")
        nodes[-1] = nodes[-1] + char
    
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
            