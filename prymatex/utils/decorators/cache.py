#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import functools
import shelve

class cacheable(object):
    flashback = None
    
    def __init__(self, stamp_function=lambda *largs, **kwargs: 0):
        self.stamp_function = stamp_function
            
    def __call__(self, func):
        full_func_name = func.__module__ + '.' + func.__name__
        @functools.wraps(func)
        def wrapped(*largs, **kwargs):
            if self.flashback is None:
                return func(*largs, **kwargs)
            key = full_func_name + str(largs) + str(kwargs)
            if key in self.flashback:
                value = self.flashback[key]
                if value[0] == self.stamp_function(*largs, **kwargs):
                    return value[1]
            retval = func(*largs, **kwargs)
            self.flashback[key] = (self.stamp_function(*largs, **kwargs), retval)
            return retval
        return wrapped

    @classmethod
    def init_cache(cls, path):
        if cls.flashback is None:
            cls.flashback = shelve.open(path, writeback=True)
    
    @classmethod
    def close_cache(cls):
        if cls.flashback is not None:
            cls.flashback.close()
            cls.flashback = None
    
    @classmethod
    def clear_cache(cls):
        if cls.falashback is not None:
            cls.flashback.clear()

if __name__ == "__main__":
    import time, random
    cacheable.init_cache('functions.cache')
   
    @cacheable(stamp_function=lambda *largs: random.choice([1]) )
    def suma(*largs):
        time.sleep(1)
        return sum(largs)

    print("Vamos a llamar una función que espera un tiempo")
    for _ in xrange(100):
        print(suma(1, 2))
    cacheable.close_cache()
