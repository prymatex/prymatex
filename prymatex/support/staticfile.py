#!/usr/bin/env python

import os

from prymatex.utils import encoding

class StaticFile(object):
    DEFAULTS = {
    'content': '''//
//  ${TM_NEW_FILE_BASENAME}
//
//  Created by ${TM_FULLNAME} on ${TM_DATE}.
//  Copyright (c) ${TM_YEAR} ${TM_ORGANIZATION_NAME}. All rights reserved.
//'''}
    def __init__(self, path, parentItem):
        self.path = path
        self.name = os.path.basename(path)
        self.parentItem = parentItem

    @classmethod    
    def type(cls):
        return cls.__name__.lower()

    def enabled(self):
        return self.parentItem.enabled()
    
    def hasSource(self, sourceName):
        return self.parentItem.hasSource(sourceName)
    
    # ----------- Update from dictionary
    def update(self, data_hash):
        for key in data_hash.keys():
            setattr(self, key, data_hash[key])
    
    # ----------- Dump to dictionary
    def dump(self, allKeys=False):
        return { 'content': self.content }

    # TODO Mejorar esto del content
    def getFileContent(self):
        content = ""
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                content = encoding.from_fs(f.read())
        return content
    
    def setFileContent(self, content):
        if os.path.exists(self.path):
            with open(self.path, 'w') as f:
                f.write(encoding.to_fs(content))
    content = property(getFileContent, setFileContent)

    def relocate(self, path):
        if os.path.exists(self.path):
            shutil.move(self.path, path)
        self.name = os.path.basename(path)
    
    def save(self, basePath = None):
        path = os.path.join(basePath, self.name) if basePath is not None else self.path
        with open(path, 'w') as f:
            f.write(encoding.to_fs(self.content))
        self.path = path
