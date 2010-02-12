#!/usr/bin/env python
#-*- encoding: utf-8 -*-
from prymatex.lib.deco import printparams, printtime

import shelve, sys

class cacheable(object):
    falashback = None
    warning_show = False
    def __call__(self, f):
        
        if cacheable.flashback is None and not cacheable.warning_show:
            sys.stderr.write("Call init_cache()\n")
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
        return sum(largs)
    
    print "Vamos a llamar una función que espera un tiempo"
    print suma(1, 2)
    print suma(1, 2)
    print suma(1, 2)
    cacheable.close_cache()