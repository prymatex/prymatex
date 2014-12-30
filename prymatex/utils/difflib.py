#!/srr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import difflib
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)

Patch = namedtuple('Patch', 'start end text')

def patches(a, b):
    sequenceMatcher = difflib.SequenceMatcher(None, a, b)
    return [ Patch(ops[1], ops[2], b[ops[3]:ops[4]]) for ops in sequenceMatcher.get_opcodes() if ops[0] != "equal" ]
    
if __name__ == '__main__':
    print(patches("uno dos tre", "uno dos tr"))
