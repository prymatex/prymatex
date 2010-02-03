#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os

class ResourceManager(QObject):
    _loaded_resources = []
    
    def __init__(self):
        self.path = os.path.dirname(__file__)
        
    def getIcon(self, path):
        # Busca primero en los fijos
        
        fpath = os.path.join(self.path, 'resources', 'icons', path)
        
        # TODO: Buscar en el tema
        # TODO: ALmacenar el icono
        print os.path.exists(fpath), fpath
        return QIcon(fpath)
    
    def changeLocale(self, locale):
        pass
    def changeTheme(self, name):
        pass
    
resource_manager = ResourceManager()

    
    