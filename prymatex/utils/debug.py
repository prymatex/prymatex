#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Debug utilities
This code was adapted from spyderlib original developed by Pierre Raybaut
spyderlib site:
http://code.google.com/p/spyderlib
"""

import io
import traceback
import time


def log_time(fd):
    timestr = "Logging time: %s" % time.ctime(time.time())
    print("="*len(timestr), file=fd)
    print(timestr, file=fd)
    print("="*len(timestr), file=fd)
    print("", file=fd)

def log_last_error(fname, context=None):
    """Log last error in filename *fname* -- *context*: string (optional)"""
    out = io.StringIO()
    traceback.print_exc(file=out)
    fd = open(fname, 'a')
    log_time(fd)
    if context:
        print("Context", file=fd)
        print("-------", file=fd)
        print("", file=fd)
        print(context, file=fd)
        print("", file=fd)
        print("Traceback", file=fd)
        print("---------", file=fd)
        print("", file=fd)
    traceback.print_exc(file=fd)
    print("", file=fd)
    print("", file=fd)

def log_dt(fname, context, t0):
    fd = open(fname, 'a')
    log_time(fd)
    print("%s: %d ms" % (context, 10*round(1e2*(time.time()-t0))), file=fd)
    print("", file=fd)
    print("", file=fd)
