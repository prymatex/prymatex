import sys

#LIB = 'ctypes_output.onig_%s' % sys.platform

#__import__(LIB, {}, {}, ['*'])

if sys.platform.count('linux2'):
    try:
        from onig_linux2 import *
    except ImportError:
        raise Exception("No oniguruma bindings found")
    
elif sys.platform.count('win32'):
    raise Exception("No support yet. Read how to port in %s"%__file__)
    