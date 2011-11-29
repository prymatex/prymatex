#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Vim integration with IPython 0.11+
#
# A two-way integration between Vim and IPython. 
#
# Using this plugin, you can send lines or whole files for IPython to execute,
# and also get back object introspection and word completions in Vim, like
# what you get with: object?<enter> object.<tab> in IPython
#
# -----------------
# Quickstart Guide:
# -----------------
# Start ipython qtconsole and copy the connection string.
# Source this file, which provides new IPython command
#   :source ipy.vim  
#   :IPythonClipboard   
#   (or :IPythonXSelection if you're using X11 without having to copy)
#
# written by Paul Ivanov (http://pirsquared.org)

reselect = False            # reselect lines after sending from Visual mode
show_execution_count = True # wait to get numbers for In[43]: feedback?
monitor_subchannel = True   # update vim-ipython 'shell' on every send?
run_flags= "-i"             # flags to for IPython's run magic when using <F5>

import sys
import os

pmx_encoding = os.environ['PMX_ENCODING'] if 'PMX_ENCODING' in os.environ and os.environ['PMX_ENCODING'] else 'utf-8'

ip = '127.0.0.1'

def km_from_string(s=''):
    """create kernel manager from IPKernelApp string
    such as '--shell=47378 --iopub=39859 --stdin=36778 --hb=52668' for IPython 0.11
    or just 'kernel-12345.json' for IPython 0.12
    """
    from os.path import join as pjoin
    from IPython.zmq.blockingkernelmanager import BlockingKernelManager, Empty
    from IPython.config.loader import KeyValueConfigLoader
    from IPython.zmq.kernelapp import kernel_aliases
    global km,send,Empty

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
        except IOError,e:
            echo(":IPython " + s + " failed", "Info")
            echo("^-- failed '" + s + "' not found", "Error")
            return
        km = BlockingKernelManager(connection_file = fullpath)
        km.load_connection_file()
    else:
        if s == '':
            echo(":IPython 0.11 requires the full connection string")
            return
        loader = KeyValueConfigLoader(s.split(), aliases=kernel_aliases)
        cfg = loader.load_config()['KernelApp']
        try:
            km = BlockingKernelManager(
                shell_address=(ip, cfg['shell_port']),
                sub_address=(ip, cfg['iopub_port']),
                stdin_address=(ip, cfg['stdin_port']),
                hb_address=(ip, cfg['hb_port']))
        except KeyError,e:
            echo(":IPython " +s + " failed", "Info")
            echo("^-- failed --"+e.message.replace('_port','')+" not specified", "Error")
            return
    km.start_channels()
    return km

def echo(arg, style="Question"):
    try:
        print arg, style
    except vim.error:
        print "-- %s" % arg
    
if __name__ == "__main__":
    connection = " ".join(sys.argv[1:])
    print connection
    kernel = km_from_string(connection)
    kernel.shell_channel.execute("a = 2")