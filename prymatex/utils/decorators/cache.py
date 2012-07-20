#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from functools import wraps
import shelve
import sys
import os

from PyQt4 import QtCore

from prymatex.utils.decorator import available_attrs, printparams, printtime

class cacheable(object):
    falashback = None
    warning_show = False
    
    def __init__(self, alteration_callback = None):
        '''
        @param alteration_callback: A callback that should check if the cached value is still valid
        The alteration_callback should return False if the value is still valid
        or the new alteration-stamp.
        modified = alteration_callback(args, current_stamp)
        
        '''
        self.alteration_callback = alteration_callback
            
    def __call__(self, f):
        
        if cacheable.flashback is None and not cacheable.warning_show:
            cacheable.warning_show = True
            return f
        
        full_func_name = f.__module__ + '.' + f.func_name
        def wrapped(*largs, **kwargs):
            key = largs + tuple(kwargs.items()) # Para que sea hasheable
            #print key
            func_memento = self.flashback.get(full_func_name, None)
            if func_memento:
                if func_memento.has_key(key):
                    return func_memento[key]
            else:
                func_memento = {}
                self.flashback[full_func_name] = func_memento
            retval = f(*largs, **kwargs)
            func_memento[key] = retval
            
            return retval
        wrapped.func_name = f.func_name
        return wrapped
    
    @classmethod
    def init_cache(cls, path):
        cls.flashback = shelve.open(path, writeback = True)
    
    @classmethod
    def close_cache(cls):
        cls.flashback.close()
    
    @classmethod
    def clear_cache(cls):
        if cls.falashback is not None:
            cls.falashback.clear()


def file_alteration_check(path):
    """Checks wether a file has changed based on its mtime and size
    """
    if os.path.isdir(path):
        pass
    elif os.path.isfile(path):
        update_time = os.stat(path)
        path = path

# {'func': {(1, 2, 4, (3, 4)): 3}} 
if __name__ == "__main__":
    import time, random
    cacheable.init_cache('functions.cache')
    print cacheable.flashback
    
    @printtime
    @printparams
    @cacheable()
    def suma(*largs):
        time.sleep(0.3)
        return sum(largs)

    
    print "Vamos a llamar una función que espera un tiempo"
    print suma(1, 2)
    print suma(1, 2)
    print suma(1, 2)
    cacheable.close_cache()
