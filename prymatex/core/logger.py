#!/srr/bin/env python
# -*- coding: utf-8 -*-

import logging

class NameFilter(logging.Filter):
    def __init__(self, pattern):
        self.pattern = pattern
        
    def filter(self, record):
        return record.name.find(self.pattern) != -1
