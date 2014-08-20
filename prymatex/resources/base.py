#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from prymatex.utils import osextra, six

LICENSES = [
    'Apache License 2.0',
    'Artistic License/GPL',
    'Eclipse Public License 1.0',
    'GNU General Public License v2',
    'GNU General Public License v3',
    'GNU Lesser General Public License',
    'MIT License',
    'Mozilla Public License 1.1',
    'New BSD License',
    'Other Open Source',
    'Other'
]

def build_resource_key(path):
    return ":/%s" % "/".join(osextra.path.fullsplit(path))
