'''
Debug breakpoints 
'''
from PyQt4.QtCore import pyqtRemoveInputHook, pyqtRestoreInputHook
import sys

try:
    import ipdb
    ipdb_available = True
except ImportError:
    ipdb_available = False
    
def ipdb_set_trace():
    '''ipdb version'''
    if not ipdb_available: return
    pyqtRemoveInputHook()
    ipdb.set_trace(sys._getframe(1))
    pyqtRestoreInputHook()