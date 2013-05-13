#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

PMX_ENCODING = os.environ['PMX_ENCODING'] if 'PMX_ENCODING' in os.environ and os.environ['PMX_ENCODING'] else 'utf-8'
PMX_IPYTHON_CONNECTION = os.environ['PMX_IPYTHON_CONNECTION'] if 'PMX_IPYTHON_CONNECTION' in os.environ else ''

ip = '127.0.0.1'

def km_from_string(s = PMX_IPYTHON_CONNECTION):
    """create kernel manager from IPKernelApp string
    such as '--shell=47378 --iopub=39859 --stdin=36778 --hb=52668' for IPython 0.11
    or just 'kernel-12345.json' for IPython 0.12
    """
    from os.path import join as pjoin
    from IPython.zmq.blockingkernelmanager import BlockingKernelManager
    from IPython.config.loader import KeyValueConfigLoader
    from IPython.zmq.kernelapp import kernel_aliases
    
    s = s.replace('--existing', '')
    if 'connection_file' in BlockingKernelManager.class_trait_names():
        from IPython.lib.kernel import find_connection_file
        # 0.12 uses files instead of a collection of ports
        # include default IPython search path
        # filefind also allows for absolute paths, in which case the search
        # is ignored
        try:
            # XXX: the following approach will be brittle, depending on what
            # connection strings will end up looking like in the future, and
            # whether or not they are allowed to have spaces. I'll have to sync
            # up with the IPython team to address these issues -pi
            if '--profile' in s:
                k,p = s.split('--profile')
                k = k.lstrip().rstrip() # kernel part of the string
                p = p.lstrip().rstrip() # profile part of the string
                fullpath = find_connection_file(k,p)
            else:
                fullpath = find_connection_file(s.lstrip().rstrip())
        except IOError as e:
            print(":IPython " + s + " failed", "Info")
            print("^-- failed '" + s + "' not found", "Error")
            return
        km = BlockingKernelManager(connection_file = fullpath)
        km.load_connection_file()
    else:
        if s == '':
            print(":IPython 0.11 requires the full connection string")
            return
        loader = KeyValueConfigLoader(s.split(), aliases=kernel_aliases)
        cfg = loader.load_config()['KernelApp']
        try:
            km = BlockingKernelManager(
                shell_address=(ip, cfg['shell_port']),
                sub_address=(ip, cfg['iopub_port']),
                stdin_address=(ip, cfg['stdin_port']),
                hb_address=(ip, cfg['hb_port']))
        except KeyError as e:
            print(":IPython " +s + " failed", "Info")
            print("^-- failed --"+e.message.replace('_port','')+" not specified", "Error")
            return
    km.start_channels()
    return km

kernelManager = km_from_string()

def get_child_msg(msg_id):
    # XXX: message handling should be split into its own process in the future
    while True:
        # get_msg will raise with Empty exception if no messages arrive in 1 second
        m = kernelManager.shell_channel.get_msg(timeout = 1)
        if m['parent_header']['msg_id'] == msg_id:
            break
        else:
            #got a message, but not the one we were looking for
            print('skipping a message on shell_channel','WarningMsg')
    return m

def execute(command):
    msg_id = kernelManager.shell_channel.execute(command)
    from pprint import pformat
    try:
        child = get_child_msg(msg_id)
        count = child['content']['execution_count']
        message = "In[%d]: %s\n" % (count, command)
        if child['content']['status'] == "ok":
            if child['content']['payload']:
                message += "\n".join([payload['text'] for payload in child['content']['payload']])    
        return message
    except Exception as e:
        return "In[]: %s\n(no reply from IPython kernel)\n%s" % (command, e)