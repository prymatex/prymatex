#!/usr/bin/env python
# encoding: utf-8

def prefix_match(lhs, rhs):
    if len(lhs) > len(rhs):
        return False

    for i in range(len(lhs)):
        if lhs[i] != rhs[i] and lhs[i] != "*":
            return False
    return True

class ScopeType(object):
    def __init__(self):
        self.anchor_to_previous = False
        self.atoms = ()

    @classmethod
    def factory(cls, atoms):
        scope = cls()
        scope.atoms = tuple(atoms.split("."))
        return scope
    
    def __str__(self):
        ret = self.anchor_to_previous and "> " or ""
        return ret + ".".join(self.atoms)

    def __repr__(self):
        return "%s anchor_to_previous:%s\n[%s]" % (self.__class__.__name__, self.anchor_to_previous, "\n".join([repr(a) for a in self.atoms]))

    def __hash__(self):
        return hash(self.anchor_to_previous) + hash(self.atoms)
    
    def __eq__(self, rhs):
        return self.atoms == rhs.atoms
    
    def __ne__(self, rhs):
        return not self == rhs
    
    def __lt__(self, rhs):
        return self.atoms < rhs.atoms
    
    def __add__(self, rhs):
        return ScopeType(self.atoms + rhs.atoms)
    
class PathType(object):
    def __init__(self):
        self.anchor_to_bol = False
        self.anchor_to_eol = False
        self.scopes = ()

    @classmethod
    def factory(cls, scopes):
        path = cls()
        path.scopes = tuple([ ScopeType.factory(scope) for scope in scopes])
        return path
    
    def __str__(self):
        ret = self.anchor_to_bol and "^ " or ""
        ret += " ".join([str(s) for s in self.scopes])
        ret += self.anchor_to_eol and " $" or ""
        return ret

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
        return PathType(self.scopes + rhs.scopes)
    
    def does_match(self, lhs, path, rank = None):
        i = len(path.scopes)
        size_i = i
        j = len(self.scopes)
        size_j = j;
        anchor_to_bol = self.anchor_to_bol
        anchor_to_eol = self.anchor_to_eol
        check_next = False
        reset_score = 0
        score = 0.0
        power = 0.0
        while j <= i and j:
            assert i; assert j
            assert i-1 < len(path.scopes)
            assert j-1 < len(self.scopes)
            anchor_to_previous = self.scopes[j-1].anchor_to_previous
            
            if (anchor_to_previous or (anchor_to_bol and j == 1)) and not check_next:
                reset_score = score
                reset_i = i
                reset_j = j
                
            power += len(path.scopes[i-1].atoms)
            if prefix_match(self.scopes[j-1].atoms, path.scopes[i-1].atoms):
                for k in range(len(self.scopes[j-1].atoms)):
                    score += 1 / pow(2, power - k)
                j -= 1
                check_next = anchor_to_previous
            elif check_next:
                i = reset_i
                j = reset_j
                score = reset_score
                check_next = False
            i -= 1;
            if anchor_to_eol:
                if i != size_i and j == size_j:
                    break;
                else:
                    anchor_to_eol = False

            if anchor_to_bol and j == 0 and i != 0:
                i = reset_i - 1
                j = reset_j
                score = reset_score
                check_next = False
            
        if j == 0 and rank is not None:
            rank.append(score)
        return j == 0

class GroupType(object):
    def __init__(self):
        self.selector = SelectorType()

    def __str__(self):
        return "(%s)" % self.selector

    def __repr__(self):
        return "%s\n[%s]" % (self.__class__.__name__, repr(self.selector))

    def __hash__(self):
        return hash(self.selector)

    def does_match(self, lhs, rhs, rank = None):
        return self.selector.does_match(lhs, rhs, rank)

class FilterType(object):
    def __init__(self, fltr):
        self.selector = SelectorType()
        self.fltr = fltr

    def __str__(self):
        return "%s:%s" % (self.fltr, self.selector)

    def __repr__(self):
        return "%s fltr:%s\n[%s]" % (self.__class__.__name__, self.fltr, repr(self.selector))

    def __hash__(self):
        return hash(self.selector) + hash(self.fltr)
    
    def does_match(self, lhs, rhs, rank = None):
        if self.fltr == 'B' and rank is not None:
            r1 = []
            r2 = []
            if self.selector.does_match(lhs, lhs, r1) and self.selector.does_match(rhs, rhs, r2):
                rank.append(max(r1.pop(), r2.pop()))
                return True
            return False
        else:
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
        ret += str(self.selector)
        return ret
    
    def __repr__(self):
        return "%s op:%s negate:%s\n[%s]" % (self.__class__.__name__, self.op, self.negate, repr(self.selector))
    
    def __hash__(self):
        return hash(self.selector) + hash(self.op) + hash(self.negate)
    
class CompositeType(object):
    def __init__(self):
        self.expressions = []
    
    def __str__(self):
        return " ".join([str(c) for c in self.expressions])
    
    def __repr__(self):
        return "%s\n[%s]" % (self.__class__.__name__, "\n".join([repr(e) for e in self.expressions]))
            
    def __hash__(self):
        return hash(self.expressions)
    
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
        return  ", ".join([str(c) for c in self.composites])

    def __repr__(self):
        return "%s\n[%s]" % (self.__class__.__name__, "\n".join([repr(c) for c in self.composites]))

    def __hash__(self):
        return hash(self.composites)
    
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
