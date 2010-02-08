#!/usr/bin/env python
#-*- encoding: utf-8 -*-



import os, plistlib
import sys
from cStringIO import StringIO

PRIMATEX_BASE_PATH = os.path.abspath(os.path.curdir)
PRYMATEX_SETTINGS_FILE = os.path.join(PRIMATEX_BASE_PATH , "settings.plist")

PROTECTED_KEYS = ('_wrapped_dict', )

class SettingsNode(object):
    
    def __init__(self, wrapped_dict, parent = None, *largs, **kwargs):
        object.__setattr__(self, '_wrapped_dict',  wrapped_dict)
        object.__setattr__(self, '_parent',  parent)
        
    def __str__(self):
        return str(self._wrapped_dict)
    
    def __setattr__(self, name, value):
        if name in PROTECTED_KEYS:
            print "Prot"
            return object.__setattr__(self, name, value)
        
        self._wrapped_dict[name] = value
        # TODO: Hacer funcionar esto
        root = self.root
        if root:
            hook = getattr(root, '_update_key_hook', None)
            if callable(hook):
                hook(name, value)
    
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
        parent, prev = self._parent, None
        while parent != None:
            prev = self._parent
            parent = parent._parent
        return prev
        
    
    def __getattr__(self, name):
        
        try:
            object.__getattr__(self, name)
        except AttributeError:
            try:
                val = self._wrapped_dict[name]
                if isinstance(val, dict):
                    return SettingsNode(val, parent = self)
                return val
            except KeyError:
                return AttributeError("%s object has no %s attribute",
                                      type(self), name )
class Settings(SettingsNode):
    '''
    Configuración gerarquica basada en diccionarios.
    '''
    TEXTMATE_BUNDLES_PATH = os.path.join(PRIMATEX_BASE_PATH, 'Bundles')
    TEXTMATE_THEMES_PATH = os.path.join(PRIMATEX_BASE_PATH, 'Themes')
    
    def __init__(self, parent = None, **defaults):
        if os.path.exists(PRYMATEX_SETTINGS_FILE):
            cfg = plistlib.readPlist(PRYMATEX_SETTINGS_FILE)
        else:
            cfg = {}
        object.__setattr__(self, '_wrapped_dict', cfg)
        object.__setattr__(self, '_parent', None)
        object.__setattr__(self, '_modified', False)
        object.__setattr__(self, '_child_settings',  {})
        
        
    def save(self):
        s = StringIO()
        try:
            plistlib.writePlist(self._wrapped_dict, s)
        except Exception, e:
            s.close()
            raise e
        else:
            f = open(PRYMATEX_SETTINGS_FILE, 'w')
            f.write(s.read())
            f.close()
            s.close()
             
    
    
    def __str__(self):
        from pprint import pformat
        return pformat(self._config)
    
    __unicode__ = __str__
    
    def update(self, iterable,**kwargs):
        '''
            D.update(E, **F) -> None.  Update D from dict/iterable E and F.
            If E has a .keys() method, does:     for k in E: D[k] = E[k]
            If E lacks .keys() method, does:     for (k, v) in E: D[k] = v
            In either case, this is followed by: for k in F: D[k] = F[k]
        '''
        raise NotImplementedError("TODO :(")
    
    
    def toJSON(self):
        pass
    
    def fromJSON(self):
        pass 
    
        
#settings = Settings()

if __name__ == '__main__':
    '''
        settings = Settings()
        settings.editor.window.x = 40
        settings.editor.window.y = 600
        settings.editor.window.width = 500
        
    '''
    settings = Settings()
    print settings.TEXTMATE_BUNDLES_PATH
    #Ponemos algo en settings, efecto configuracion de usuario
    #settings._update_key_hook = lambda key, val: sys.stout.write("Event: %s = %s" % (key, value))
    print settings.TEXTMATE_THEMES_PATH
    settings.pepe = 3
    settings.editor = {'window':{'x': 30, 'y': 50, 'height': 500, 'width':600}}
    print "settings.editor.window.x = ", settings.editor.window.x 
    settings.editor.window.x = 128
    print "Root", settings.root
    print "settings.editor.window.x = ", settings.editor.window.x
    
    #print settings.editor.window
    settings.config_vars = dict(TEXTMATE_THEMES_PATH = '/pepe/algo/Themes',
                                TEXTMATE_COMPAT_MODE = 'supercompat :P')
    #print settings
    settings.save()