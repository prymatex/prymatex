#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import zmq
import argparse
import tempfile
import re
from multiprocessing import Process, Queue

from multiplexer import Multiplexer

CONNECTION = re.compile(r"(?P<protocol>.*)\:\/\/(?P<host>[^:/ ]+).?(?P<port>[0-9]*)")

# ===========
# = Workers =
# ===========
def worker_multiplexer(queue, addr):
    multiplexer = Multiplexer(queue)
    
    context = zmq.Context()
    zrep = context.socket(zmq.REP)
    
    match = CONNECTION.match(addr)
    if not match:
        return

    parts = match.groupdict()
    if not parts["port"] and parts["protocol"] in ["tcp", "udp"]:
        parts["port"] = zrep.bind_to_random_port(addr)
        queue.put("%(protocol)s://%(host)s:%(port)s" % parts)
    else:
        zrep.bind(addr)
        queue.put(addr)
    
    while True:
        pycmd = zrep.recv_pyobj()
        method = getattr(multiplexer, pycmd["command"], None)
        if method is not None:
            zrep.send_pyobj(method(*pycmd["args"]))
        else:
            zrep.send_pyobj(None)


def worker_notifier(queue, addr):
    context = zmq.Context()
    zpub = context.socket(zmq.PUB)
    
    match = CONNECTION.match(addr)
    if not match:
        return

    parts = match.groupdict().copy()
    if not parts["port"] and parts["protocol"] in ["tcp", "udp"]:
        parts["port"] = zpub.bind_to_random_port(addr)
        queue.put("%(protocol)s://%(host)s:%(port)s" % parts)
    else:
        zpub.bind(addr)
        queue.put(addr)
    
    while True:
        data = queue.get()
        zpub.send(data)


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
    parser.add_argument('-t', metavar='<type>', dest='type', type=str, default="ipc", help=HELP['type'])
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
    elif args.type == "tcp":
        address = args.address if args.address is not None else 'localhost'
        pub_addr = "tcp://%s" % address
        rep_addr = "tcp://%s" % address
        if args.pub_port is not None:
            pub_addr += ":%i" % args.pub_port
        if args.rep_port is not None:
            rep_addr += ":%i" % args.rep_port
    return rep_addr, pub_addr

def main(args):
    
    rep_addr, pub_addr = get_addresses(args)
    
    if rep_addr and pub_addr:
        queue = Queue()
    
        # Start the multiplexer
        mproc = Process(target=worker_multiplexer, args=(queue, rep_addr))
        mproc.start()
        
        # Start the notifier
        nproc = Process(target=worker_notifier, args=(queue, pub_addr))
        nproc.start()
        
        a1, a2 = queue.get(), queue.get()
        print a1, a2
    else:    
        print "Address error, please read help"

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
