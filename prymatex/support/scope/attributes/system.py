#!/usr/bin/env python

import platform

def attributes(filePath, projectDirectory = None):
    return [ "attr.os-version." + platform.release() ]
