#!/usr/bin/env python

import os

from collections import namedtuple

class Source(namedtuple('Source', 'name path time')):
    def __new__(cls, name, path, time=0):
        if os.path.exists(path):
            time = os.path.getmtime(path)
        return super(Source, cls).__new__(cls, name, path, time)

    def hasChanged(self):
        time = self.exists and os.path.getmtime(self.path) or 0
        return self.time != time
    
    def newPath(self, path):
        time = self.exists and os.path.getmtime(path) or 0
        return self._replace(path=path, time=time)

    def newUpdatedTime(self):
        time = self.exists and os.path.getmtime(self.path) or 0
        return self._replace(time=time)

    @property
    def exists(self):
        return os.path.exists(self.path)