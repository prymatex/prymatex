#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import zmq
import argparse
import stat
import signal
import tempfile

from multiprocessing import Process, Queue
from multiplexer import Multiplexer
    
# ===========
# = Workers =
# ===========
def worker_multiplexer(queue_multiplexer, queue_notifier, addr):
    multiplexer = Multiplexer(queue_notifier)
        
    context = zmq.Context()
    zrep = context.socket(zmq.REP)
    
    if addr[1]:
        port = zrep.bind_to_random_port(addr[0])
        queue_multiplexer.put("%s:%d" % (addr[0], port))
    else:
        zrep.bind(addr[0])
        queue_multiplexer.put(addr[0])
    
    while True:
        pycmd = zrep.recv_pyobj()
        method = getattr(multiplexer, pycmd["command"], None)
        if method is not None:
            zrep.send_pyobj(method(*pycmd["args"]))
        else:
            zrep.send_pyobj(None)


def worker_notifier(queue_notifier, addr):
    context = zmq.Context()
    zpub = context.socket(zmq.PUB)
    
    if addr[1]:
        port = zpub.bind_to_random_port(addr[0])
        queue_notifier.put("%s:%d" % (addr[0], port))
    else:
        zpub.bind(addr[0])
        queue_notifier.put(addr[0])
        
    while True:
        data = queue_notifier.get()
        zpub.send_multipart(data)


# ==============
# = Parse args =
# ==============
DESCRIPTION = 'pmxterm backend.'

# Dictionary of command-line help messages
HELP = {
    'rep_port': 'Port number of the request/responce socket',
    'pub_port': 'Port number of the publisher socket',
    'type': 'The zmq socket type "ipc", "tcp"',
    'address': 'TCP and UDP bind address'
}

def parse_arguments():
    """Creates argument parser for parsing command-line arguments. Returns parsed
    arguments in a form of a namespace.
    """
    # Setting up argument parses
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-t', metavar='<type>', dest='type', type=str, default="tcp", help=HELP['type'])
    parser.add_argument('-a', metavar='<address>', dest='address', type=str, help=HELP['address'])
    parser.add_argument('-pp', metavar='<pub_port>', dest='pub_port', type=int, help=HELP['pub_port'])
    parser.add_argument('-rp', metavar='<rep_port>', dest='rep_port', type=int, help=HELP['rep_port'])
    args = parser.parse_args()
    if args.type == "ipc" and args.address is not None:
        parser.print_help()
        sys.exit()
    return args

def get_addresses(args):
    pub_addr = rep_addr = None
    if args.type == "ipc":
        pub_addr = "ipc://%s" % tempfile.mkstemp(prefix="pmx")[1]
        rep_addr = "ipc://%s" % tempfile.mkstemp(prefix="pmx")[1]
        return (rep_addr, False), (pub_addr, False)
    elif args.type == "tcp":
        address = args.address if args.address is not None else '127.0.0.1'
        pub_addr = "tcp://%s" % address
        rep_addr = "tcp://%s" % address
        pub_port = rep_port = True
        if args.pub_port is not None:
            pub_port = False
            pub_addr += ":%i" % args.pub_port
        if args.rep_port is not None:
            rep_port = False
            rep_addr += ":%i" % args.rep_port
        return (rep_addr, rep_port), (pub_addr, pub_port)
    return None, None

if __name__ == "__main__":
    rep_addr, pub_addr = get_addresses(parse_arguments())

    if not rep_addr or not pub_addr:
        print "Address error, please read help"
        sys.exit(-1)

    queue_multiplexer = Queue()
    queue_notifier = Queue()
    
    # Start the notifier
    nproc = Process(target=worker_notifier, args=(queue_notifier, pub_addr))
    nproc.start()

    naddress = queue_notifier.get()    
    
    # Start the multiplexer
    mproc = Process(target=worker_multiplexer, args=(queue_multiplexer, queue_notifier, rep_addr))
    mproc.start()
    
    maddress = queue_multiplexer.get()
        
    info = { "multiplexer": maddress, "notifier": naddress }
    
    print "To connect another client to this backend, use:"
    print info
    sys.stdout.flush()
    
    def signal_handler(signal, frame):
        nproc.terminate()
        mproc.terminate()
        sys.exit(0)
    
    if sys.platform.startswith("linux"):
        signal.signal(signal.SIGINT, signal_handler)
    elif sys.platform == "win32":
        signal.signal(signal.SIGBREAK, signal_handler)
