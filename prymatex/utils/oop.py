# -*- encoding: utf-8 -*-

## {{{ http://code.activestate.com/recipes/412551/ (r1)
class Singleton(type):
    def __init__(self, *args):
        type.__init__(self, *args)
        self._instances = {}

    def __call__(self, *args):
        if not args in self._instances:
            self._instances[args] = type.__call__(self, *args)
        return self._instances[args]


## end of http://code.activestate.com/recipes/412551/ }}}
