#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created: 04/02/2010 by defo

#http://en.wikipedia.org/wiki/Unix_signal

import os, re, signal
import unicodedata
import string
from prymatex.utils import six

from subprocess import PIPE, Popen

ps_output = re.compile('''
      #PID TTY          TIME CMD      
      #1 ?        00:00:00 init
      (?P<pid>\d{1,6})\s*(?P<tty>[\d\w\?\/]+)\s*(?P<time>[\d\:]+)\s*(?P<name>[\d\w\/\<\>\s]+)   
''', re.VERBOSE| re.IGNORECASE)

SIGNALS = dict([(keyname, getattr(signal, keyname)) for keyname in dir(signal) if keyname.startswith('SIG')])
VALID_PATH_CARACTERS = "-_.() %s%s" % (string.ascii_letters, string.digits)

def ps_proc_dict():
    proc = Popen("ps -ea".split(), stdout=PIPE)
    proc.wait()
    proc_list = []
    for l in  proc.stdout.readlines():
        match = ps_output.search(l.strip())
        if match:
            proc_list.append(match.groupdict())
    return proc_list

def pid_proc_dict():
    d = {}
    for proc in ps_proc_dict():
        pid = int(proc.pop('pid'))
        d[pid] = proc
    return d

def to_valid_name(name):
    name = unicodedata.normalize('NFKD', six.text_type(name)).encode('ASCII', 'ignore')
    return "".join([ c for c in name if c in VALID_PATH_CARACTERS ])

if __name__ == "__main__":
    from pprint import pprint
    pprint(ps_proc_dict())
    