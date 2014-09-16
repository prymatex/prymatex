#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from prymatex.utils import osextra

def build_resource_key(path):
    return ":/%s" % "/".join(osextra.path.fullsplit(path))
