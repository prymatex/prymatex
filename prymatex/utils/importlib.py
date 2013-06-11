#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in range(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level package")
    return "%s.%s" % (package[:dot], name)


def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]

def import_from_directory(directory, name):
    """ 
    Import a module from directory
    """
    #TODO: ver si el modulo ya esta importado, quiza con solo un reload alcanza
    #TODO: ver como usar esta funcion con "with"
    sys.path.insert(1, directory)
    try:
        module = import_module(name)
        reload(module) # Might be out of date
    except ImportError as reason:
        print(reason)
        raise reason
    finally:
        del sys.path[1]
    return module