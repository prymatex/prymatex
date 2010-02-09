
'''
Manejo de señales
'''
from PyQt4.QtGui import qApp

def publish(signal_name, *larsg, **kwargs):
    qApp.instance().emit()
    
    
def register_callback(name, callback):
    pass

class register(object):
    '''
    Function decorator for signal registration
    
    '''
    def __init__(self, name):
        self.name = name
        
    def __call__(self, f):
        def wrapped(*largs, **kwargs):
            retval = f(*largs, **kwargs)
            return retval
        return wrapped
        