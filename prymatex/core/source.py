#!/usr/bin/env python

import os

from collections import namedtuple

class Source(namedtuple('Source', 'name path time')):
    def __new__(cls, name, path, time=0):
        return super(Source, cls).__new__(cls,
            name,
            path,
            os.path.exists(path) and os.path.getmtime(path) or 0)

    def getTime(self):
        return self.exists() and os.path.getmtime(self.path) or 0
        
    def hasChanged(self):
        return self.time != self.getTime()
    
    def newPath(self, path):
        time = self.exists() and os.path.getmtime(path) or 0
        return self._replace(path=path, time=time)

    def newUpdateTime(self):
        return self._replace(time=self.getTime())

    def exists(self):
        return os.path.exists(self.path)