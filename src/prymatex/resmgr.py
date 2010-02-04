#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os

class ResourceManager(QObject):
    __loaded_resources = []
    __current_theme = None
    __current_theme_path = None
    
    def __init__(self):
        self.path = os.path.dirname(__file__)
        # TODO: Cargar por confgiuracion
        self.current_theme = self.available_themes[0]
        
    
    def current_theme(): #@NoSelf
        def fget(self):
            return self.__current_theme
        def fset(self, value):
            self.__current_theme = value
            self.__current_theme_path = os.path.join(self.path, 'resources', 'themes', value)
        return locals()
    current_theme = property(**current_theme())
    
    @property
    def current_theme_path(self):
        return self.__current_theme_path 
    
    @property
    def available_themes(self):
        theme_path = os.path.join(self.path, 'resources', 'themes') 
        print os.path.exists(theme_path)
        for _dirpath, dirnames, _filenames in os.walk(theme_path):
            return dirnames
            
    
    def getIcon(self, path):
        # Busca primero en los fijos
        
        fpath = os.path.join(self.path, 'resources', 'icons', path)
        if not os.path.exists(fpath):
            fpath = os.path.join(self.current_theme_path, 'icons', path)
            
        
#        if os.path.exists(fpath):
#            print path, "->", fpath
        # TODO: ALmacenar el icono
        print os.path.exists(fpath), fpath
        
        return QIcon(fpath)
    
    def changeLocale(self, locale):
        pass
    def changeTheme(self, name):
        pass
    
resource_manager = ResourceManager()

    
    