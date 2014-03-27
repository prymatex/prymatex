#!/srr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import logging

logger = logging.getLogger(__name__)

def read_file(path):
    try:
        with open(path, 'r') as fp:
            return json.load(fp)
    except Exception as exc:
        logger.error('Error reading json file %s' % path)
        logger.error(exc)

def write_file(structure, path, indent=2):
    with open(path, 'w') as fp:
        json.dump(structure, fp, sort_keys=True,
            indent=indent, separators=(',', ': '))
