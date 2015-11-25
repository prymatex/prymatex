#!/usr/bin/env python
import os
from prymatex.core import config

class Project(object):
    KEYS = ( 'name', 'description', 'licence', 'keywords', 'source_folders', 
            'shell_variables', 'bundles', 'namespace_folders' )
    def __init__(self, path, manager):
        self.path = path
        self.manager = manager
    
    # ---------------- Load, update, dump
    def __load_update(self, data_hash, initialize):
        dirname = os.path.dirname(self.path())
        for key in Project.KEYS:
            if key in data_hash or initialize:
                value = data_hash.pop(key, None)
                if value is None and key in ('source_folders', 'bundles', 'namespace_folders'):
                    value = []
                if key in ('source_folders', 'namespace_folders'):
                    value = [
                        os.path.normpath(
                            os.path.join(dirname, os.path.expanduser(v))
                        ) for v in value ]
                setattr(self, key, value)

    def load(self, data_hash):
        self.__load_update(data_hash, True)

    def update(self, data_hash):
        self.__load_update(data_hash, False)

    def dump(self, allKeys=False):
        data_hash = { }
        dirname = os.path.dirname(self.path )
        for key in Project.KEYS:
            value = getattr(self, key, None)
            if allKeys or value:
                if key in ("source_folders", "namespace_folders"):
                    value = [
                        re.sub(
                            "^%s" % config.USER_HOME_PATH, "~", os.path.relpath(v, dirname)
                        ) for v in value ]
                data_hash[key] = value
        return data_hash
        