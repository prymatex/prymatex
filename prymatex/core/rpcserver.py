#!/usr/bin/env python
#-*- encoding: utf-8 -*-

# TODO: Constants!

from SimpleXMLRPCServer import SimpleXMLRPCServer
from PyQt4.Qt import QThread
from prymatex.core.base import PMXObject

PORT = 4612

class PMXCommandDispatcher(PMXObject):
    
    def nib(self, args):
        print "nib: ", args
        return True
    
    def tooltip(self, args):
        '''
        tm_dialog tooltip --transparent --text|--html CONTENT
        '''
        print "Tooltip: ", args
        return True
    
    def menu(self, args):
        print "menu: ", args
        return True
    
    def popup(self, args):
        print "popup: ", args
        return True
    
    def images(self, args):
        print "images: ", args
        return True
    
    def alert(self, args):
        print "alert: ", args
        return True
    
    def debug(self, options, args):
        print "debug: ", options, args
        return True

class PMXXMLRPCServerThread(QThread):
    def __init__(self, parent):
        super(PMXXMLRPCServerThread, self).__init__(parent)
        self.server = SimpleXMLRPCServer(('', PORT),
                                         encoding = 'utf-8')
        self.dispatcher = PMXCommandDispatcher()
        self.server.register_instance(self.dispatcher)
    
    def run(self):
        self.server.serve_forever()

    