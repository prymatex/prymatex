#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys
import imp
try:
    import builtins
except ImportError as ex:
    import __builtin__ as builtins

_baseimport = builtins.__import__
_dependencies = dict()
_parent = None

def _import(name, globals=None, locals=None, fromlist=None, level=-1):
    # Track our current parent module.  This is used to find our current
    # place in the dependency graph.
    global _parent
    parent = _parent
    _parent = name

    # Perform the actual import using the base import function.
    if sys.version_info.major == 3 and level < 0:
        level = 0
    m = _baseimport(name, globals, locals, fromlist, level)

    # If we have a parent (i.e. this is a nested import) and this is a
    # reloadable (source-based) module, we append ourself to our parent's
    # dependency list.
    if parent is not None and hasattr(m, '__file__'):
        l = _dependencies.setdefault(parent, [])
        l.append(m)

    # Lastly, we always restore our global _parent pointer.
    _parent = parent

    return m

def get_dependencies(m):
    """Get the dependency list for the given imported module."""
    return _dependencies.get(m.__name__, None)

def _reload(m, visited):
    """Internal module reloading routine."""
    name = m.__name__

    # Start by adding this module to our set of visited modules.  We use
    # this set to avoid running into infinite recursion while walking the
    # module dependency graph.
    visited.add(m)

    # Start by reloading all of our dependencies in reverse order.  Note
    # that we recursively call ourself to perform the nested reloads.
    deps = _dependencies.get(name, None)
    if deps is not None:
        for dep in reversed(deps):
            if dep not in visited:
                _reload(dep, visited)

    # Clear this module's list of dependencies.  Some import statements
    # may have been removed.  We'll rebuild the dependency list as part
    # of the reload operation below.
    try:
        del _dependencies[name]
    except KeyError:
        pass

    # Because we're triggering a reload and not an import, the module
    # itself won't run through our _import hook.  In order for this
    # module's dependencies (which will pass through the _import hook) to
    # be associated with this module, we need to set our parent pointer
    # beforehand.
    global _parent
    _parent = name

    # Perform the reload operation.
    imp.reload(m)

    # Reset our parent pointer.
    _parent = None

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

def reload_module(m):
    """Reload an existing module.

    Any known dependencies of the module will also be reloaded."""
    _reload(m, set())

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

    # Reeplace builtin __import__
    builtins.__import__ = _import

    if name in sys.modules:
        reload_module(sys.modules[name])
    else:
        __import__(name)

    # Restore builtin __import__
    builtins.__import__ = _baseimport

    return sys.modules[name]

def import_from_directories(directories, name, remove = False):
    """Import a module from directory"""
    sys.path = sys.path[:1] + directories + sys.path[1:]
    try:
        module = import_module(name)
    except ImportError as reason:
        print(reason)
        raise reason
    finally:
        if remove:
            del sys.path[1:len(directories) + 1]
    return module
