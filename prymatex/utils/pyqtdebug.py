'''
Debug breakpoints 
'''
from PyQt4.QtCore import pyqtRemoveInputHook, pyqtRestoreInputHook
import sys


def ipdb_set_trace():
    '''ipdb version'''
    try:
        import ipdb
    except ImportError:
        pass
    else:
        pyqtRemoveInputHook()
        ipdb.set_trace(sys._getframe(1))
        pyqtRestoreInputHook()