#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created: 04/02/2010 by defo

import os
from subprocess import PIPE, Popen
import re
import user

ps_output = re.compile('''
      #PID TTY          TIME CMD      
      #1 ?        00:00:00 init
      (?P<pid>\d{1,6})\s*(?P<tty>[\d\w\?\/]+)\s*(?P<time>[\d\:]+)\s*(?P<name>[\d\w\/\<\>\s]+)   
''', re.VERBOSE| re.IGNORECASE)

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

def get_homedir():
    return user.home
    
if __name__ == "__main__":
    from pprint import pprint
    pprint(ps_proc_dict())
    