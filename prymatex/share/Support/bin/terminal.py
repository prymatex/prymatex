#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import zmq
import sys 

PORT = 4613

class TerminalHandler(object):
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('tcp://127.0.0.1:%d' % PORT)
        
    def run(self, command):
        command = {"name": "runCommand", "args": [ command ], "kwargs": {}}
        self.socket.send_pyobj(command)
        value = self.socket.recv_pyobj()
        sys.stdout.write(value["result"])
    
def main(args):
    handler = TerminalHandler()
    if len(args) >= 1:
        handler.run(" ".join(args))

if __name__ == '__main__':
    main(sys.argv[1:])