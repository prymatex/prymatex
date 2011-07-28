# coding: utf-8

# TODO: Constants!

from SimpleXMLRPCServer import SimpleXMLRPCServer
from PyQt4.Qt import QThread
from prymatex.core.base import PMXObject

PORT = 4612

class PMXCommandDispatcher(PMXObject):
    
    def show_tooltip(self, transparent, format, content):
        print "Tooltip: ", content
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

    