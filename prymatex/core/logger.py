#!/srr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

from datetime import datetime

from .config import (PMX_LOG_FORMAT, PMX_LOG_DATE_FORMAT,
    PMX_LOG_DATETIME_FORMAT, DEBUG)

LOGGING_LEVELS = [
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG,
    logging.NOTSET
]

class NameFilter(logging.Filter):
    def __init__(self, pattern):
        self.pattern = pattern
        
    def filter(self, record):
        return record.name.find(self.pattern) != -1

def config(verbose, directory, namePattern=None):
    level = LOGGING_LEVELS[verbose % 5]
    # Prepara logging

    # File name
    filename = os.path.join(directory, 
        '%s.log' % datetime.now().strftime(PMX_LOG_DATE_FORMAT))
    logging.basicConfig(filename=filename, level= DEBUG and logging.DEBUG or logging.WARNING)

    # Console handler
    console = logging.StreamHandler()
    formatter = logging.Formatter(PMX_LOG_FORMAT, PMX_LOG_DATETIME_FORMAT)
    console.setFormatter(formatter)
    console.setLevel(level)

    if namePattern:
        #Solo al de consola
        console.addFilter(NameFilter(namePattern))

    logging.root.addHandler(console)

def getLogger(*largs, **kwargs):
    return logging.getLogger(*largs, **kwargs)
