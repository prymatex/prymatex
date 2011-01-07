#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Snippte's module
'''

from prymatex.bundles.syntax import PMXSyntax
from prymatex.bundles.processor import PMXDebugSyntaxProcessor
from prymatex.bundles.base import PMXBundleItem

class PMXSnippet(PMXBundleItem):
    def __init__(self, hash, name_space = "default"):
        super(PMXSnippet, self).__init__(hash, name_space)
        for key in [    'content', 'disableAutoIndent', 'inputPattern', 'bundlePath' ]:
            setattr(self, key, hash.pop(key, None))
            

def parse_file(filename):
    import plistlib
    data = plistlib.readPlist(filename)
    return PMXSnippet(data)

if __name__ == '__main__':
    import os
    from glob import glob
    files = glob(os.path.join('../share/Bundles/', '*'))
    for f in files:
        snippets = glob(os.path.join(f, 'Snippets/*'))
        for s in snippets:
            try:
                snippet = parse_file(s)
                parser.parse(snippet.content, PMXDebugSyntaxProcessor())
            except Exception, e:
                print "Error in %s, %s" % (s, e)stlib
    data = plistlib.readPlist(filename)
    return PMXSnippet(data)

if __name__ == '__main__':
    import os
    from glob import glob
    files = glob(os.path.join('../share/Bundles/', '*'))
    for f in files:
        snippets = glob(os.path.join(f, 'Snippets/*'))
        for s in snippets:
            try:
                snippet = parse_file(s)
                parser.parse(snippet.content, PMXDebugSyntaxProcessor())
            except