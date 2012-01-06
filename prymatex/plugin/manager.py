#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Based on http://www.qtcentre.org/wiki/index.php?title=Extended_Main_Window

from prymatex.gui.utils import textToObjectName

class PMXPluginManager(object):
    def __init__(self):
        self.class_map = {"editor": {},
                          "docker": {}
                          }
        self.instances = {"editor":{},
                          "docker": {}
                          }
    
    def register(self, key, widget_class):
        # last one in wins
        keys = key.split(".")
        ns = self.class_map
        for key in keys[:-1]:
            ns = ns.get(key)
        ns[keys[-1]] = widget_class
 
    def instance(self, key, instance = 0):
        keys = key.split(".")
        ns = self.instances
        for key in keys[:-1]:
            ns = ns.get(key)
            
        if keys[-1] not in ns:
            return None
        return ns[keys[-1]][instance]

    def createEditor(self, editor_name, filePath, project):
        if editor_name not in self.class_map["editor"]:
            raise LookupError('The editor "%s" has not been registered' % editor_name)
 
        widget = self.class_map["editor"][editor_name].newInstance(filePath, project)
        widget.setObjectName(textToObjectName(widget.tabTitle(), sufix = "Editor"))
        
        #TODO: Quitarlo de las instancias cuando se cierra
        self.instances["editor"].setdefault(editor_name, [])
        self.instances["editor"][editor_name].append(widget)
        return widget