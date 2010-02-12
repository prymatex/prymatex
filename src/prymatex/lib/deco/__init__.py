# -*- encoding: utf-8 -*-

'''
Some useful decorators
'''

from time import time

def printparams(f):
    def wrapped(*largs, **kwargs):
        dict_repr = [ "%s=%s" % (k, v) for k, v in kwargs.iteritems()]
        args = ', '.join(map(str, largs) + dict_repr)
        print "%s(%s)" % (f.func_name, args)
        retval = f(*largs, **kwargs)
        
        return retval
    wrapped.func_name = f.func_name
    return wrapped

def printtime(f):
    def wrapped(*largs, **kwargs):
        t0 = time()
        retval = f(*largs, **kwargs)
        print "%s tomó %.7f s" % (f.func_name, time()-t0)
        return retval
    wrapped.func_name = f.func_name
    return wrapped 