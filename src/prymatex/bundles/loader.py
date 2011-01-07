#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 09/02/2010 by defo

from PyQt4.QtCore import QThread, SIGNAL
from PyQt4.QtGui import qApp
from os.path import abspath, join
import os
from glob import glob
from bundle import load_prymatex_bundle

def path2bundlename(path):
    if path.endswith(os.sep):
        path = path[:-1]
    rindex = path.rindex(os.sep)
    name = path[rindex:]
    return name.split('.')[0]

class PMXBundleLoaderThread(QThread):
    def __init__(self, path_list, parnet):
        QThread.__init__(self, parnet)
        
        if isinstance(path_list, basestring):
            path_list = [ path_list, ]
        self.path_list = path_list
    
    def run(self):
        # Carga de los bundles
        self.setPriority(self.IdlePriority)
        for path in self.path_list:
            search_path = join(abspath(path), '*.tmbundle')
            bundles = glob(search_path)
            
        #    for bundle_path in bundles:
        #        qApp.emit(SIGNAL('bundleAvailable'), path2bundlename(bundle_path))
                
            # Con eso se podrían llenar los menus
            for bundle_path in bundles:
                name = path2bundlename(bundle_path) 
                try:
                    bundle = load_prymatex_bundle(bundle_path)
                except:
         #           qApp.emit(SIGNAL('bundleFailed'), name)
                    pass
                else:
                    #qApp.emit(SIGNAL('bundleLoaded'), name, bundle)
                    pass
                # Intentamos que nos se freeze la interfase
                qApp.processEvents()
        
               for bundle_path in bundles:
                name = path2bundlename(bundle_path) 
                try:
                    bundle = load_prymatex_bundle(bundle_path)
                except:
         #           qApp.emit(SIGNAL('bundleFailed'), name)
                    pass
                else:
                    #qApp.emit(SIGNAL('bundleLoaded'), name, bundle)
                    pass
                #