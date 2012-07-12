#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import warnings
from functools import wraps

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function %s." % func.__name__, category=DeprecationWarning)
        return func(*args, **kwargs)
    return new_func