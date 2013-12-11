#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# ----------------- Python Source tests --------------------
def is_builtin(text):
    """Test if passed string is the name of a Python builtin object"""
    import builtins
    return text in [str(name) for name in dir(__builtin__)
                    if not name.startswith('_')]

def is_keyword(text):
    """Test if passed string is the name of a Python keyword"""
    import keyword
    return text in keyword.kwlist
