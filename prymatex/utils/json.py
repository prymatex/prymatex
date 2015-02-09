#!/srr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import logging
import re

# Regular expression for comments
comment_re = re.compile(
    '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
)

logger = logging.getLogger(__name__)

dumps = lambda obj, indent = 2, separators=(',', ': '), **kwargs: \
	json.dumps(obj, indent = indent, separators = separators, **kwargs)

loads = lambda source, **kwargs: json.loads(source, **kwargs)

dump = lambda obj, fp, indent=2, separators=(',', ': '), **kwargs: \
	json.dump(obj, fp, indent=indent, separators=separators, **kwargs)

load = lambda fp, **kwargs: json.load(fp, **kwargs)
    
def read_file(path):
    try:
        with open(path, 'r') as fp:
            content = ''.join(fp.readlines())
            ## Looking for comments
            match = comment_re.search(content)
            while match:
                # single line comment
                content = content[:match.start()] + content[match.end():]
                match = comment_re.search(content)
            return loads(content)
    except Exception as exc:
        logger.error('Error reading json file %s' % path)
        logger.error(exc)

def write_file(obj, path, **kwargs):
    with open(path, 'w') as fp:
        dump(obj, fp, **kwargs)
