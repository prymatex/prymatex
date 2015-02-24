#!/usr/bin/env python

import sys
import re

CODE_PATTERN = re.compile(r"\.icon-([\w-]+):before{content:'\\([0-9A-Fa-f]+)'}")

TEMPLATE = """#!/usr/bin/env python
import sys

if sys.version_info[0] == 3:
    unichr = chr

#You can use the names on the page http://www.webhostinghub.com/glyphs/bootstrap/
_codepoints = [ 
%(codepoints)s ]
%(name)s = dict(( (code[0], unichr(code[1])) for code in _codepoints ))
"""

def read_less(path):
    with open(path, 'r') as f:
        return f.read().splitlines()

def main(argv):
    codepoints = []
    for line in read_less('whhg.css'):
        match = CODE_PATTERN.match(line)
        if match:
            codepoints.append("    ('%s', 0x%s)" % match.groups())
    print(TEMPLATE % {'codepoints': ',\n'.join(codepoints), 'name': 'WebHostingHub_Glyphs'})
    
if __name__ == '__main__':
    main(sys.argv)
