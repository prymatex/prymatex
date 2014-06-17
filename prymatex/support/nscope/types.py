#!/usr/bin/env python
# encoding: utf-8

from functools import reduce

def prefix_match(lhs, rhs):
    if len(lhs) > len(rhs):
        return False
    
    for l, r in zip(lhs.split("."), rhs.split(".")):
        if l != r and l != "*":
            return False

    return True

class ScopeType(object):
    def __init__(self):
        self.anchor_to_previous = False
        self.atoms = ""

    def __str__(self):
        ret = self.anchor_to_previous and "> " or ""
        return ret + self.atoms

    __unicode__ = __str__
    
    def __repr__(self):
        return "%s anchor_to_previous:%s\n[%s]" % (self.__class__.__name__, self.anchor_to_previous, self.atoms)

    def __hash__(self):
        return hash(self.anchor_to_previous) + hash(self.atoms)
    
    def __eq__(self, rhs):
        return self.atoms == rhs.atoms
    
    def __ne__(self, rhs):
        return not self == rhs
    
    def __lt__(self, rhs):
        return self.atoms.count(".") < rhs.atoms.count(".")
    
    def __add__(self, rhs):
        scope = ScopeType()
        scope.atoms = "%s %s" (self.atoms, rhs.atoms)
        return scope
    
class PathType(object):
    def __init__(self):
        self.anchor_to_bol = False
        self.anchor_to_eol = False
        self.scopes = []

    def __str__(self):
        ret = self.anchor_to_bol and "^ " or ""
        ret += " ".join(("%s" % scope for scope in self.scopes))
        ret += self.anchor_to_eol and " $" or ""
        return ret

    __unicode__ = __str__
    
    def to_open_xml(self):
        return "".join(("<%s>" % scope for scope in self.scopes))

    def to_close_xml(self):
        return "".join(("</%s>" % scope for scope in self.scopes[::-1]))
                
    def __repr__(self):
        return "%s anchor_to_bol:%s anchor_to_eol:%s\n[%s]" % (self.__class__.__name__, self.anchor_to_bol, self.anchor_to_eol, "\n".join([repr(s) for s in self.scopes]))

    def __hash__(self):
        return hash(self.anchor_to_bol) + hash(self.anchor_to_eol) + hash(self.scopes)

    def __eq__(self, rhs):
        return self.scopes == rhs.scopes
    
    def __ne__(self, rhs):
        return self.scopes != rhs.scopes
    
    def __lt__(self, rhs):
        return self.scopes < rhs.scopes
    
    def __add__(self, rhs):
        path = PathType()
        path.scopes = self.scopes + rhs.scopes
        return path
    
    def does_match(self, unused, scope, rank = None):
        node = scope.node
        sel_index = len(self.scopes) - 1
        sel = self.scopes[sel_index]
        score = 0.0
        
        btNode = None
        btSelector_index = -1
        btSelector = None
        btScore = 0.0

        power = 0.0

        if self.anchor_to_eol:
            while node and node.is_auxiliary_scope():
                if rank is not None:
                    power += node.number_of_atoms()
                node = node.parent
            btSelector_index = sel_index
            btSelector = self.scopes[sel_index]

        while node and sel_index != -1:
            if rank is not None:
                power += node.number_of_atoms()

            isRedundantNonBOLMatch = self.anchor_to_bol and node.parent and sel_index - 1 == -1
            if not isRedundantNonBOLMatch and prefix_match(sel.atoms, node):
                if sel.anchor_to_previous:
                    if btSelector_index == -1:
                        btNode = node
                        btSelector_index = sel_index
                        btSelector = sel
                        btScore = score
                elif btSelector_index != -1:
                    btSelector_index = -1

                if rank is not None:
                    score = reduce(
                        lambda s, k: s + (1.0 / pow(2, power - k)),
                        range(sel.atoms.count("."), -1, -1),
                        score
                    )

                sel_index -= 1
                sel = self.scopes[sel_index]
            elif btSelector_index != -1:
                if not btNode:
                    break
                node = btNode
                sel_index = btSelector_index
                score = btScore
                sel = btSelector
                btSelector_index = -1
                btSelector = None
            node = node.parent

        if rank is not None:
    	    rank.append(sel_index == -1 and score or 0)

        return sel_index == -1

class GroupType(object):
    def __init__(self):
        self.selector = SelectorType()

    def __str__(self):
        return "(%s)" % self.selector

    __unicode__ = __str__

    def __repr__(self):
        return "%s\n[%s]" % (self.__class__.__name__, repr(self.selector))

    def __hash__(self):
        return hash(self.selector)

    # Listo
    def does_match(self, lhs, rhs, rank = None):
        return self.selector.does_match(lhs, rhs, rank)

class FilterType(object):
    def __init__(self, fltr):
        self.selector = SelectorType()
        self.fltr = fltr

    def __str__(self):
        return "%s:%s" % (self.fltr, self.selector)

    __unicode__ = __str__

    def __repr__(self):
        return "%s fltr:%s\n[%s]" % (self.__class__.__name__, self.fltr, repr(self.selector))

    def __hash__(self):
        return hash(self.selector) + hash(self.fltr)
    
    # Listo
    def does_match(self, lhs, rhs, rank = None):
        if self.fltr == 'B' and rank is not None:
            r1 = []
            r2 = []
            if self.selector.does_match(lhs, lhs, r1) and self.selector.does_match(rhs, rhs, r2):
                rank.append(max(r1.pop(), r2.pop()))
                return True
            return False
        if self.fltr == 'L':
            return self.selector.does_match(lhs, lhs, rank)
        elif self.fltr == 'R':
            return self.selector.does_match(rhs, rhs, rank)
        elif self.fltr == 'B':
            return self.selector.does_match(lhs, lhs, rank) and self.selector.does_match(rhs, rhs, rank)
        return False
        
class ExpressionType(object):
    def __init__(self, op):
        self.op = op
        self.negate = False
        self.selector = SelectorType()
    
    def __str__(self):
        ret = self.op is not None and "%s " % self.op or ""
        ret += self.negate and "-" or ""
        ret += "%s" % self.selector
        return ret

    __unicode__ = __str__

    def __repr__(self):
        return "%s op:%s negate:%s\n[%s]" % (self.__class__.__name__, self.op, self.negate, repr(self.selector))
    
    def __hash__(self):
        return hash(self.selector) + hash(self.op) + hash(self.negate)
    
class CompositeType(object):
    def __init__(self):
        self.expressions = []
    
    def __str__(self):
        return " ".join(("%s" % expression for expression in self.expressions))

    __unicode__ = __str__

    def __repr__(self):
        return "%s\n[%s]" % (self.__class__.__name__, "\n".join([repr(e) for e in self.expressions]))
    
    # Listo
    def does_match(self, lhs, rhs, rank = None):
        res = False
        if rank is not None:
            rsum = 0
            r = []
            for expr in self.expressions:
                op = expr.op
                local = expr.selector.does_match(lhs, rhs, r)
                if local:
                    rsum = max(r.pop(), rsum)
                if expr.negate:
                    local = not local
                
                if op is None:
                    res = local
                elif op == '|':
                    res = res or local
                elif op == '&':
                    res = res and local
                elif op == '-':
                    res = res and not local
            if res:
                rank.append(rsum)
            return res
        else:
            for expr in self.expressions:
                op = expr.op
                if res and op == '|':   # skip ORs when we already have a true value
                    continue
                elif not res and op == '&':  # skip ANDs when we have a false value
                    continue
                elif not res and op == '-':  # skip intersection when we have a false value
                    continue
                
                local = expr.selector.does_match(lhs, rhs, rank)
                if expr.negate:
                    local = not local

                if op is None:
                    res = local
                elif op == '|':
                    res = res or local
                elif op == '&':
                    res = res and local
                elif op == '-':
                    res = res and not local
            return res
    
class SelectorType(object):
    def __init__(self):
        self.composites = []
        
    def __str__(self):
        return  ", ".join(("%s" % composite for composite in self.composites))

    __unicode__ = __str__

    def __repr__(self):
        return "%s\n[%s]" % (self.__class__.__name__, "\n".join([repr(c) for c in self.composites]))

    def __hash__(self):
        return hash(self.composites)
    
    # Listo
    def does_match(self, lhs, rhs, rank = None):
        if rank is not None:
            res = False
            rsum = 0
            r = []
            for composite in self.composites:
                if composite.does_match(lhs, rhs, r):
                    rsum = max(r.pop(), rsum)
                    res = True
            if res:
                rank.append(rsum)
            return res
        for composite in self.composites:
            if composite.does_match(lhs, rhs, rank):
                return True
        return False
