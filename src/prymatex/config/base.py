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

PMX_BASE_PATH = get_prymatex_base_path()
PMX_USER_PATH = get_prymatex_user_path()
PMX_SETTINGS_FILE = os.path.join(PMX_USER_PATH , "settings.plist")

PROTECTED_KEYS = ('_wrapped_dict', '_setting')

class Setting(object):
    def __init__(self, name, value = None, default = None):
        self.name = name
        self.value = value
        self.default = default
    
    def to_python(self):
        return self.value

    def contribute_to_class(self, cls):
        self.fget = getattr(cls, self.name, None)
        self.fset = getattr(cls, "set%s" % self.name.title(), None)
        setattr(cls, self.name, self)
        
    def __get__(self, instance, instance_type = None):
        if instance == None:
            return self.value or self.default
        elif hasattr(self, 'fget'):
            return self.fget(instance)
    
    def __set__(self, instance, value):
        if isinstance(instance, Setting):
            self.value = value
        else:
            self.fset(instance, value)

class SettingsNode(object):
    def __init__(self, items = {}, subitems = {}):
        __wrapped_items = {}
        __wrapped_subitems = {}
        for key, value in items.iteritems():
            __wrapped_items[key] = Setting(key, value = value)
        for key, value in subitems.iteritems():
            __wrapped_subitems[key] = SettingsNode(**value)
        self.__dict__['__wrapped_items'] = __wrapped_items
        self.__dict__['__wrapped_subitems'] = __wrapped_subitems
        self.__dict__['__instances'] = []
    
    def __setattr__(self, name, value):
        if name in self.__dict__['__wrapped_items'].keys():
            item = self.__dict__['__wrapped_items'][name]
            item.__set__(item, value)
            for instance in self.__dict__['__instances']:
                item.__set__(instance, value)
        else:
            raise AttributeError
    
    def __getattr__(self, name, default = None):
        if self.__dict__['__wrapped_items'].has_key(name):
            item = self.__dict__['__wrapped_items'][name]
            return item.__get__(item)
        elif self.__dict__['__wrapped_subitems'].has_key(name):
            return self.__dict__['__wrapped_subitems'][name]
        elif default != None:
            return default
        raise AttributeError
            
    def setdefault(self, name, defaults = {}):
        node = self.__dict__['__wrapped_subitems'].setdefault(name, SettingsNode())
        for k, v in defaults.iteritems():
            if node.__dict__['__wrapped_items'].has_key(k):
                node.__dict__['__wrapped_items'][k].default = v
            else:
                node.__dict__['__wrapped_items'][k] = Setting(k, default = v)
        return node

    def to_python(self):
        result = {}
        items = filter(lambda t: t[1], map(lambda (k, v): (k, v.to_python()), self.__dict__['__wrapped_items'].iteritems()))
        subitems = filter(lambda t: t[1], map(lambda (k, v): (k, v.to_python()), self.__dict__['__wrapped_subitems'].iteritems()))
        if items:
            result['items'] = dict(items)
        if subitems:
            result['subitems'] = dict(subitems)
        return result
    
    def add_to_class(self, cls):
        setattr(cls, 'settings', self)
        for setting in self.__dict__['__wrapped_items'].values():
            setting.contribute_to_class(cls)
    
    def add_instance(self, instance):
        self.__dict__['__instances'].append(instance)
    
class Settings(SettingsNode):
    '''
    Configuración gerarquica basada en diccionarios.
    '''
    PMX_BUNDLES_PATH = os.path.join(PMX_BASE_PATH, 'share', 'Bundles')
    PMX_THEMES_PATH = os.path.join(PMX_BASE_PATH, 'share', 'Themes')
    PMX_SUPPORT_PATH = os.path.join(PMX_BASE_PATH, 'share', 'Support')
    
    def __init__(self, **defaults):
        if os.path.exists(PMX_SETTINGS_FILE):
            wrapped = plistlib.readPlist(PMX_SETTINGS_FILE)
        else:
            wrapped = {}
        super(Settings, self).__init__(**wrapped)
        
    def save(self):
        obj = self.to_python()
        plistlib.writePlist(obj, PMX_SETTINGS_FILE)

settings = Settings()

class PMXOptions(object):
    def __init__(self, options=None):
        self.settings = getattr(options, 'settings', None)
        self.events = getattr(options, 'events', None)

class PersonaBase(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(PersonaBase, cls).__new__(cls, name, bases, attrs)
        opts = new_class._meta = PMXOptions(getattr(new_class, 'Meta', None))
        if opts.settings:
            sns = settings
            for base in bases:
                if hasattr(base._meta, 'settings') and base._meta.settings != None:
                    sns = getattr(sns, base._meta.settings[0])
            class_settings = sns.setdefault(*opts.settings)
            class_settings.add_to_class(new_class)
        return new_class

if __name__ == "__main__":
    class Persona():
        __metaclass__ = PersonaBase
        def __init__(self, nombre):
            self.nombre = nombre
            self.settings.add_instance(self)

    class Empleado(Persona):
        def __init__(self, nombre):
            super(Empleado, self).__init__(nombre)

        def cargo(self): 
            return self._cargo
        
        def setCargo(self, cargo):
            print "poniendo cargo" 
            self._cargo = cargo
            
        def sueldo(self):
            return self._sueldo

        def setSueldo(self, sueldo):
            print "poniendo sueldo"
            self._sueldo = sueldo

        class Meta(object):
            events = ('uno', 'dos', )
            settings = ('empleado', {   'cargo': 'Programador Jr.',
                                        'sueldo': 100 })
            
    class Jefe(Empleado):
        def __init__(self, nombre):
            super(Jefe, self).__init__(nombre)
            
        class Meta(object):
            events = ('uno', 'dos', )
            settings = ('jefe', { 'sueldo': 200 })
    
    j = Jefe("Caho")
    e = Empleado("Caho")
    settings.empleado.sueldo = 8000
    print e.sueldo