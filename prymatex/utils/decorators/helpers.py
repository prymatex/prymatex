#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from time import time
import functools

def format_args(*largs, **kwargs):
    dict_repr = [ "%s=%s" % (k, repr(v)) for k, v in kwargs.iteritems()]
    args = ', '.join(map(repr, largs) + dict_repr)
    return args

def printparams(function):
    @functools.wraps(function)
    def wrapped(*largs, **kwargs):
        print "%s(%s)" % (function.func_name, format_args(*largs, **kwargs))
        retval = function(*largs, **kwargs)
        return retval
    return wrapped

def printparams_and_output(function):
    @functools.wraps(function)
    def wrapped(*largs, **kwargs):
        output = "%s(%s)" % (function.func_name, format_args(*largs, **kwargs))
        retval = function(*largs, **kwargs)
        print "%s -> %s" % (output, retval)
        return retval
    return wrapped

def printtime(function):
    @functools.wraps(function)
    def wrapped(*largs, **kwargs):
        t0 = time()
        retval = function(*largs, **kwargs)
        if hasattr(function, 'im_class'):
            func_name = '.'.join([function.im_class.__name__, function.im_func.__name__]) 
        else:
            func_name = function.func_name
        print "%s tomσ %.7f s" % (func_name, time() - t0)
        return retval
    return wrapped

def _get_logger(function):
    import logging
    return logging.getLogger(function.__module__)

def logtime(function):
    @functools.wraps(function)
    def wrapped(*largs, **kwargs):
        t0 = time()
        retval = function(*largs, **kwargs)
        if hasattr(function, 'im_class'):
            func_name = '.'.join([function.im_class.__name__, function.im_func.__name__]) 
        else:
            func_name = function.func_name

        _get_logger(function).info("%s took %.7f s" % (func_name, time()-t0))
        return retval
    return wrapped