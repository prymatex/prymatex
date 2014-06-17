#!/usr/bin/env python
# encoding: utf-8

#atom:         «string» | '*'
#scope:        «atom» ('.' «atom»)*
#path:         '^'? «scope» ('>'? «scope»)* '$'?
#group:        '(' «selector» ')'
#filter:       ("L:"|"R:"|"B:") («group» | «path»)
#expression:   '-'? («filter» | «group» | «path»)
#composite:    «expression» ([|&-] «expression»)*
#selector:     «composite» (',' «composite»)*

from . import types

class Parser(object):
    def __init__(self, source):
        self.source = source
        self.it = 0
        self.last = len(source)

    def ws(self):
        while self.it != self.last and self.source[self.it] in (" ", "\t"):
            self.it += 1
        return True

    def parse_char(self, chars, dest = None):
        if self.it == self.last or self.source[self.it] not in tuple(chars):
            return False
        if dest is not None:
            dest.append(self.source[self.it])
        self.it += 1
        return True

    def parse_scope(self, res):
        res.anchor_to_previous = self.parse_char(">") and self.ws()
        frm = self.it
        while True:
            if self.it == self.last or (not self.source[self.it].isalnum() and self.source[self.it] != '*' and ord(self.source[self.it]) < 0x80):
                break
            while self.it != self.last and (self.source[self.it].isalnum() or self.source[self.it] in ['_', '-', '+', '*'] or ord(self.source[self.it]) > 0x7F):
                self.it += 1
            if not self.parse_char("."):
                break
        res.atoms = self.source[frm:self.it]
        
        return frm != self.it

    def parse_newpath(self, res):
        path = types.PathType()
        if self.parse_path(path):
            res.composites.append(path)
            return True
        return False
        
    def parse_path(self, res):
        res.anchor_to_bol = self.parse_char("^") and self.ws()
        while True:
            scope = types.ScopeType()
            if not self.parse_scope(scope):
                break
            res.scopes.append(scope)
            if not self.ws():
                break

        res.anchor_to_eol = self.parse_char("$")
        return True

    def parse_group(self, res):
        bt = self.it
        group = types.GroupType()
        if self.parse_char("(") and self.parse_selector(group.selector) and self.ws() and self.parse_char(")"):
            res.composites.append(group)
            return True
        self.it = bt
        return False

    def parse_filter(self, res):
        bt = self.it
        dest = []
        if self.parse_char("LRB", dest) and self.parse_char(":") and self.ws():
            fltr = types.FilterType(dest and dest[0] or None)
            if self.parse_group(fltr.selector) or self.parse_newpath(fltr.selector):
                res.composites.append(fltr)
                return True
        self.it = bt
        return False

    def parse_expression(self, res):
        if self.parse_char("-") and self.ws():
            res.negate = True
        return self.parse_filter(res.selector) or self.parse_group(res.selector) or self.parse_newpath(res.selector)

    def parse_composite(self, res):
        rc = False
        dest = []
        while True:
            expression = types.ExpressionType(dest and dest.pop() or None)
            if not self.parse_expression(expression):
                break
            res.expressions.append(expression)
            rc = True
            if self.ws() and self.parse_char("&|-", dest) and self.ws():
                continue
            break
        return rc

    def parse_selector(self, res):
        rc = False
        self.ws()
        while True:
            composite = types.CompositeType()
            if not self.parse_composite(composite):
                break
            res.composites.append(composite)
            rc = True
            if not (self.ws() and self.parse_char(",") and self.ws()):
                break
        return rc
    
    # = API =
    @staticmethod
    def selector(source):
        selector = types.SelectorType()
        if Parser(source).parse_selector(selector):
            return selector

