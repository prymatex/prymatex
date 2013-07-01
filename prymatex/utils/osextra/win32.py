#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Windows Instrumentation Interfase
# http://coding.derkeiler.com/Archive/Python/comp.lang.python/2008-07/msg00947.html
# http://timgolden.me.uk/python/wmi/index.html

import wmi
import os
instrumentation = wmi.WMI()

def pid_proc_dict():
    '''
    @note: This shuold be implemented on every platform
    @note: Should be tested on every platform
    '''

    d = {}
    procs = instrumentation.Win32_Process()
    for proc in procs:
        pid = getattr(proc, 'ProcessId')
        d[pid] = proc
    return d

# TODO Filter names like lpt, com, etc
def to_valid_name(self, name):
    name = unicodedata.normalize('NFKD', six.text_type(name)).encode('ASCII', 'ignore')
    return "".join([ c for c in name if c in VALID_PATH_CARACTERS ])

def get_homedir():
    return os.environ.get('USERPROFILE')

if __name__ == "__main__":
    from pprint import pprint
    pprint(pid_proc_dict())