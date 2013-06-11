'''
Monitor filesystem changes to be notified to apps
Possible backend could be:
    - Thread, like Django does
    - inotify on Linux systems
    - ???
'''

class PMXFileMonitor(object):
    pass


from prymatex.qt.QtCore import QThread

class PMXThreadFileMonitor(PMXFileMonitor, QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        PMXFileMonitor.__init__(self)
        
    def addPath(self, filepath, filter):
        pass
    
    
    
    
    
    