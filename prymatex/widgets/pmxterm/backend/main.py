#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import stat
import signal
import tempfile
import constants
import socket
import json
import queue

from multiprocessing import Process, Queue
from multiprocessing.reduction import recv_handle, send_handle
from multiplexer import Multiplexer

queue_multiplexer = Queue()
queue_notifier = Queue()
procs = set()
shutdown = False

# ===========
# = Workers =
# ===========
def worker_multiplexer(queue_multiplexer, queue_notifier):
    global shutdown

    def debug(*args, **kwargs):
        print(args, kwargs)

    multiplexer = Multiplexer(queue_notifier)
    while not shutdown:
        pycmd = queue_multiplexer.get()
        getattr(multiplexer, pycmd["command"], debug)(*pycmd["args"])
        if pycmd['command'] == 'buried_all':
            break
    multiplexer.stop()

def worker_notifier(queue_notifier):
    global shutdown
    
    channels = {}
    while not shutdown:
        message = queue_notifier.get()
        if message['cmd'] == 'send':
            channel = channels[message['channel']]
            data = json.dumps(message['payload']).encode(constants.FS_ENCODING)
            channel.send(data)
            channel.send(b"\n\n")
        elif message['cmd'] == 'buried_all':
            for channel in channels.values():
                channel.close()
            break
        elif message['cmd'] == 'setup_channel':
            s = socket.socket(socket.AF_UNIX)
            s.connect(message['address'])
            channels[message['channel']] = s
            
def worker_client(queue_multiplexer, queue_notifier, sock):
    global shutdown

    _id = sock.fileno()
    while not shutdown:
        data = sock.recv(4096)
        pycmd = json.loads(data.decode(constants.FS_ENCODING))
        pycmd["args"].insert(0, _id)
        queue_multiplexer.put(pycmd)
        if pycmd['command'] == 'buried_all':
            break

def get_addresses(args):
    pub_addr = rep_addr = None
    if args.type == "unix":
        return "%s" % tempfile.mktemp(prefix="pmx")
    elif args.type == "inet":
        address = args.address if args.address is not None else '127.0.0.1'
        return (address, 0)
    return None

# Install singla handler
def signal_handler(signum, frame):
    global shutdown
    shutdown = True
    queue_multiplexer.close()
    queue_notifier.close()
    for proc in procs:
        proc.terminate()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
if sys.platform == "win32":
    signal.signal(signal.SIGBREAK, signal_handler)

if __name__ == "__main__":
    # Creates argument parser for parsing command-line arguments.
    parser = argparse.ArgumentParser(description="Prymatex's terminal backend.")
    parser.add_argument('-t', metavar='<type>', dest='type', type=str, 
        default="unix", help='The zmq socket type "unix", "inet"'
    )
    parser.add_argument('-a', metavar='<address>', dest='address',
        type=str, help='Bind address'
    )
    parser.add_argument('-p', metavar='<port>', dest='pub_port',
        type=int, help='Port number of the socket'
    )
    args = parser.parse_args()
    if args.type == "unix" and args.address is not None:
        parser.print_help()
        sys.exit()
    
    address = get_addresses(args)
    
    if not isinstance(address, (str, tuple)):
        parser.print_help()
        sys.exit(-1)

    server = socket.socket(args.type == "unix" and socket.AF_UNIX or socket.AF_INET)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server.bind(address)
    server.listen(5)

    print("To connect a client to this backend, use:")
    print(json.dumps({'address': server.getsockname()}))
    sys.stdout.flush()
    
    # Start the multiplexer
    mproc = Process(target=worker_multiplexer,
        args=(queue_multiplexer, queue_notifier), name="multiplexer"
    )
    mproc.start()
    procs.add(mproc)

    # Start the notifier
    nproc = Process(target=worker_notifier,
        args=(queue_notifier, ), name="notifier"
    )
    nproc.start()
    procs.add(nproc)
    while not shutdown:
        try:
            conn, address = server.accept()
        except InterruptedError:
            continue

        # Start the notifier
        cproc = Process(target=worker_client, 
            args=(queue_multiplexer, queue_notifier, conn), name="client"
        )
        cproc.start()
        procs.add(cproc)
        
        conn.close()