#!/usr/bin/env python
#-*- encoding: utf-8 -*-

# TODO: Constants!
import plistlib
from SimpleXMLRPCServer import SimpleXMLRPCServer
from PyQt4.Qt import QThread
from prymatex.core.base import PMXObject

PORT = 4612

class PMXCommandDispatcher(PMXObject):
    
    def nib(self, options, args):
        print "nib: ", options, args
        return True
    
    def tooltip(self, options, args):
        print "Tooltip: ", options, args
        return True
    
    def menu(self, options, args):
        print "menu: ", options, args
        return True
    
    def popup(self, options, args):
        print "popup: ", options, args
        return True
    
    def defaults(self, options, args):
        print "defaults: ", options, args
        return True
    
    def images(self, options, args):
        print "images: ", options, args
        return True
    
    def alert(self, options, args):
        print "alert: ", options, args
        return True
    
    def debug(self, options, args):
        print "debug: ", options, args
        return plistlib.writePlistToString({"selectedIndex": 1})

class PMXXMLRPCServerThread(QThread):
    def __init__(self, parent):
        super(PMXXMLRPCServerThread, self).__init__(parent)
        self.server = SimpleXMLRPCServer(('', PORT),
                                         encoding = 'utf-8')
        self.dispatcher = PMXCommandDispatcher()
        self.server.register_instance(self.dispatcher)
    
    def run(self):
        self.server.serve_forever()

    