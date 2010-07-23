#!/usr/bin/env python
#-*- encoding: utf-8 -*-
from prymatex.lib.exceptions import ConfigNotFound

import os, plistlib

PRIMATEX_BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PRYMATEX_SETTINGS_FILE = os.path.join(PRIMATEX_BASE_PATH , "settings.plist")

class Settings(object):
    def __init__(self, config_file = None, **defaults):
        self.config_file = config_file or PRYMATEX_SETTINGS_FILE 
        
        if os.path.exists(self.config_file):
            config = plistlib.readPlist(self.config_file)
            
        else:
            config = dict(
                          TEXTMATE_THEMES_PATHS = [os.path.join(PRIMATEX_BASE_PATH, 'resources', 'Themes')],
                          TEXTMATE_BUNDLES_PATHS = [os.path.join(PRIMATEX_BASE_PATH, 'resources', 'Bundles')],
            )
            config.update(defaults)
                
        for key, value in config.iteritems():
            setattr(self, key, value)
        
    def __getattr__(self, name):
        return self.__dict__.get(name, self.__class__.__dict__.get(name)) 
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
    
    def save(self):
        plistlib.writePlist(self.__dict__, self.config_file)
    
    def __str__(self):
        return str(self.__dict__)
        
settings = Settings()

if __name__ == '__main__':
    print settings
    #Ponemos algo en settings, efecto configuracion de usuario
    settings.save()