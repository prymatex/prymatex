#!/usr/bin/env python
#-*- encoding: utf-8 -*-

"""Some useful decorators
"""

from prymatex.utils.decorators.helpers import printparams, printparams_and_output, printtime, logtime
from prymatex.utils.decorators.deprecated import deprecated

from functools import WRAPPER_ASSIGNMENTS

def available_attrs(fn):
    """
    Return the list of functools-wrappable attributes on a callable.
    This is required as a workaround for http://bugs.python.org/issue3445.
    """
    return tuple(a for a in WRAPPER_ASSIGNMENTS if hasattr(fn, a))
