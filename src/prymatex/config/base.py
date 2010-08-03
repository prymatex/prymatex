#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os, plistlib

def get_prymatex_base_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_prymatex_user_path():
    path = os.path.join(os.path.expanduser("~"), ".prymatex")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

PRIMATEX_BASE_PATH = get_prymatex_base_path()
print PRIMATEX_BASE_PATH
PRIMATEX_USER_PATH = get_prymatex_user_path()
PRYMATEX_SETTINGS_FILE = os.path.join(PRIMATEX_BASE_PATH , "settings.plist")

PROTECTED_KEYS = ('_wrapped_dict', )

class SettingsNode(object):
    
    def __init__(self, wrapped_dict, parent = None):
        self._wrapped_dict = wrapped_dict
        self.__dict__['_parent'] = parent
        self.__dict__['_modified'] = False
        
    def __setattr__(self, name, value):
        if name in PROTECTED_KEYS:
            self.__dict__['_wrapped_dict'] = dict()
            for k, v in value.iteritems():
                setattr(self, k, v)
        elif isinstance(value, dict):
            self.__dict__['_wrapped_dict'][name] = SettingsNode(value, parent = self)
        else:
            self.__dict__['_wrapped_dict'][name] = value
    
    @property
    def namespace(self):
        keys = []
        parent, prev = self._parent, None
        while parent != None:
            prev = self._parent
            for key, value in prev._wrapped_dict.iteritems():
                if value == self._wrapped_dict:
                    keys.append(key)
                    break
            parent = parent._parent
        return '.'.join(keys)

    @property
    def root(self):
        root = self
        while root._parent != None:
            root = root._parent
        return root
    
    def __getattr__(self, name, default = None): 
        try:
            return self.__dict__['_wrapped_dict'][name]
        except KeyError:
            if default == None:
                setattr(self, name, {})
                return self.__dict__['_wrapped_dict'][name]
            else:
                setattr(self, name, default)
        return default
    
    def to_python(self):
        ret = {}
        for k, v in self.__dict__['_wrapped_dict'].iteritems():
            if hasattr(v, 'to_python'):
                ret[k] = v.to_python()
            else:
                ret[k] = v
        return ret
    
class Settings(SettingsNode):
    '''
    Configuración gerarquica basada en diccionarios.
    '''
    TEXTMATE_BUNDLES_PATH = [os.path.join(PRIMATEX_BASE_PATH, 'resources', 'Bundles'), os.path.join(PRIMATEX_USER_PATH, 'Bundles')]
    TEXTMATE_THEMES_PATH = [os.path.join(PRIMATEX_BASE_PATH, 'resources', 'Themes'), os.path.join(PRIMATEX_USER_PATH, 'Themes')]
    
    def __init__(self, parent = None, **defaults):
        if os.path.exists(PRYMATEX_SETTINGS_FILE):
            wrapped_dict = plistlib.readPlist(PRYMATEX_SETTINGS_FILE)
        else:
            wrapped_dict = {}
        super(Settings, self).__init__(wrapped_dict)
        
    def save(self):
        obj = self.to_python()
        plistlib.writePlist(obj, PRYMATEX_SETTINGS_FILE)

settings = Settings()