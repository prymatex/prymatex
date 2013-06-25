#!/usr/bin/env python

import platform

def attributes():
    return "attr.os-version." + platform.release()
