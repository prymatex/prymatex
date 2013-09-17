#!/srr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime

LOGGING_LEVELS = [
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG
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
    filename = os.path.join(directory, '%s-%s.log' % (
        logging.getLevelName(level), datetime.now().strftime('%d-%m-%Y')))
    logging.basicConfig(filename=filename, level=level)

    # Console handler
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    ch.setLevel(level)

    if namePattern:
        #Solo al de consola
        ch.addFilter(NameFilter(namePattern))

    logging.root.addHandler(ch)

def getLogger(*largs, **kwargs):
    return logging.getLogger(*largs, **kwargs)
