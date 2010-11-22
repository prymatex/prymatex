# -*- encoding: utf-8 -*-

'''
Some useful decorators
'''

from time import time

# Taken from http://wiki.python.org/moin/PythonDecoratorLibrary
# #CreatingWell-BehavedDecorators.2BAC8.22Decoratordecorator.22
def simple_decorator(decorator):
    """This decorator can be used to turn simple functions
    into well-behaved decorators, so long as the decorators
    are fairly simple. If a decorator expects a function and
    returns a function (no descriptors), and if it doesn't
    modify function attributes or docstring, then it is
    eligible to use this. Simply apply @simple_decorator to
    your decorator and it will automatically preserve the
    docstring and function attributes of functions to which
    it is applied."""
    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g
    # Now a few lines needed to make simple_decorator itself
    # be a well-behaved decorator.
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator


@simple_decorator
def printparams(f):
    def wrapped(*largs, **kwargs):
        dict_repr = [ "%s=%s" % (k, v) for k, v in kwargs.iteritems()]
        args = ', '.join(map(str, largs) + dict_repr)
        print "%s(%s)" % (f.func_name, args)
        retval = f(*largs, **kwargs)
        return retval
    return wrapped

@simple_decorator
def printtime(f):
    def wrapped(*largs, **kwargs):
        t0 = time()
        retval = f(*largs, **kwargs)
        if hasattr(f, 'im_class'):
            func_name = '.'.join([f.im_class.__name__, f.im_func.__name__]) 
        else:
            func_name = f.func_name
        print "%s tomó %.7f s" % (func_name, time()-t0)
        return retval
    return wrapped

def _get_logger(f):
    import logging
    return logging.getLogger(f.__module__)

@simple_decorator
def logtime(f):
    def wrapped(*largs, **kwargs):
        t0 = time()
        retval = f(*largs, **kwargs)
        if hasattr(f, 'im_class'):
            func_name = '.'.join([f.im_class.__name__, f.im_func.__name__]) 
        else:
            func_name = f.func_name

        _get_logger(f).info("%s took %.7f s" % (func_name, time()-t0))
        return retval
    return wrapped
