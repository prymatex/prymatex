from PyQt4.QtCore import QThread, SIGNAL
from PyQt4.QtGui import qApp
from os.path import abspath, join
import os
from bundle import load_textmate_bundle

def path2bundlename(path):
    if path.endswith(os.sep):
        path = path[:-1]
    rindex = path.rindex(os.sep)
    name = path[rindex:]
    return name.split('.')[0]

class PMXThread(QThread):
    def __init__(self, path_list, parnet):
        QThread.__init__(self, parnet)
        self.path_list = path_list
    
    def run(self):
        # Carga de los bundles
        for path in self.path_list: 
            bundles = join(abspath(path), '*.tmBundle')
            
            for bundle_path in bundles:
                qApp.emit(SIGNAL('bundleAvailable'), path2bundlename(bundle_path))
                
            # Con eso se podrían llenar los menus
            for bundle_path in bundles:
                name = path2bundlename(bundle_path) 
                try:
                    bundle = load_textmate_bundle(bundle_path)
                except:
                    qApp.emit(SIGNAL('bundleFailed'), name)
                else:
                    qApp.emit(SIGNAL('bundleLoaded'), name, bundle)
                    
    