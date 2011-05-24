# encoding: utf-8
from os.path import *
import shelve, pickle
from helpers import simple_decorator
import atexit
from functools import partial

def get_cache_location(func):
    if not hasattr(func, '__module__'):
        mod = repr(func)
        func_path = mod[mod.index("'")+1:mod.rindex("'")]
        
    else: 
        func_path = func.__module__ + '.' + func.func_name
        
    from PyQt4.QtGui import qApp
    if qApp.instance():
        return qApp.instance().getProfilePath('cache', func_path)
    return join(abspath(expanduser('~')), '.prymatex', "%s.memoize" % func_path)

def _get_memoized_value(func, args, kwargs):
    """Used internally by memoize decorator to get/store function results"""
    key = ','.join(map(repr, args) + map(repr, kwargs.items()))
  
    if not func._cache_dict.has_key(key):
        ret = func(*args, **kwargs)
        func._cache_dict[key] = ret
  
    return func._cache_dict[key]

def _get_memoized_value_dict(func, args, kwargs):
    """Used internally by memoize decorator to get/store function results"""
    key = args + kwargs.items()
  
    if not func._cache_dict.has_key(key):
        ret = func(*args, **kwargs)
        func._cache_dict[key] = ret
  
    return func._cache_dict[key]

def _save_cache(func):
    print "Saving shelve %s" % func._cache_path
    func._cache_dict.sync()

@simple_decorator
def memoize(func):
    """Decorator that stores function results in a dictionary to be used on the
    next time that the same arguments were informed."""
    func._cache_path = get_cache_location(func)
    func._cache_dict = shelve.open(func._cache_path)
    atexit.register(partial(_save_cache, func))
  
    def _inner(*args, **kwargs):
        return _get_memoized_value(func, args, kwargs)
    return _inner

def _save_cache_dict(func):
    print "Pickling cache %s" % func._cache_path
    try:
        pickle.dump(func._cache_dict, file(func._cache_path, 'w'))
    except Exception, e:
        #import ipdb; ipdb.set_trace()
        raise
        

@simple_decorator
def memoize_dict(func):
    """Decorator that stores function results in a dictionary to be used on the
    next time that the same arguments were informed."""
    func._cache_path = get_cache_location(func)
    try:
        func._cache_dict = pickle.load(file(func._cache_path))
    except Exception, e:
        func._cache_dict =  {}
    atexit.register(partial(_save_cache_dict, func))
  
    def _inner(*args, **kwargs):
        return _get_memoized_value(func, args, kwargs)
    return _inner

    
    
if __name__ == "__main__":
    from time import sleep
    from os.path import *
    from helpers import printtime
    
    @printtime
    @memoize
    def funcion(*cadenas):
        sleep(len(cadenas)* 0.1)
        return '.'.join(map(repr, cadenas))
    
    @printtime
    @memoize_dict
    def funcion2(*cadenas):
        sleep(len(cadenas)* 0.1)
        return '.'.join(map(repr, cadenas))
    
    
    
    print funcion(1, 2, 4, 5)
    print funcion(1, 2, 4, 5)
    print funcion(1, 2, 4, 5)
    print funcion(1, 2, 4, 5)
    
    print funcion2(1, 2, 4, 5)
    print funcion2(1, 2, 4, 5)
    print funcion2(1, 2, 4, 5)
    print funcion2(1, 2, 4, 5)
    
    
