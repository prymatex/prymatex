#!/usr/bin/env python
__doc__ = """
Generates some Python classes to wrap C structures

"""

__author__ = "D3f0"

import sys
import re
from os.path import exists
from optparse import OptionParser

SYNTAX_LINE_RE = re.compile('''
    \#define\s+
    ONIG_SYNTAX_(?P<name>[\w_]+)\s+
    \(\&(?P<symbol>[\w\_]+)
''', re.VERBOSE)


ENCODING_LINE_RE = re.compile('''
    \#define\s+
    ONIG_ENCODING_(?P<name>[\w_]+)\s+
    \(\&(?P<symbol>[\w\_]+)
''', re.VERBOSE)


SYNTAXES = []
ENCODINGS = []

def find_syntax(line):
    global SYNTAXES
    match = SYNTAX_LINE_RE.search(line)
    if match:
        name, symbol = match.group('name'), match.group('symbol')
        SYNTAXES.append(dict(name = name, symbol = symbol))

def find_encoding(line):
    global ENCODINGS
    match = ENCODING_LINE_RE.search(line)
    if match:
        name, symbol = match.group('name'), match.group('symbol')
        ENCODINGS.append(dict(name = name, symbol = symbol))
    
def collect(line):
    find_syntax(line)
    find_encoding(line)

    
    
    
#===============================================================================
# dump
#===============================================================================
PREFIX = \
'''
# This file is automatically generated, do not edit.
from oniguruma_cdefs cimport *
cdef class Syntax:
    cdef OnigSyntaxType syntax
    cdef inline __init__(self, OnigSyntaxType* syntax, name):
        self.name = name
        self.syntax = syntax
        
    cdef inline __str__(self):
        return "<Syntax %s>" % self.name
'''

SYNTAX_WRAPER_CLASS_TMPL = \
'''
%(name)s = Syntax(%(symbol)s, "%(name)s")
'''


def dump(output = sys.stdout):
    '''
    @param output: A file stream
    '''
    output.write(PREFIX)
    for syntax in SYNTAXES:
        output.write(SYNTAX_WRAPER_CLASS_TMPL % syntax)
        
    
    
    
        
def process_file(name, opts):
    fp = open(name, 'r')
    for line in fp.readlines():
        collect(line)
    fp.close()

def main(argv = sys.argv):
    parser = OptionParser(description = __doc__)
    parser.add_option('-o', '--outout', dest = "output", 
                      help = "Output file", default = None)
    parser.add_option('-f', '--force', action = "store_true", 
                      help = "Force overwrite", default = False)
    opts, files = parser.parse_args( argv[1:] )
    
    if not files:
        sys.stderr.write("No file given\n")
        return -1
    
    if opts.output:
        
        if exists(opts.output) and not opts.force:
            sys.stderr.write("%d alrady exists. Please use -f to overwirte\n")
            return -2
        output = file(opts.output, 'w')
    else:
        output = sys.stdout
            
    for name in files:
        process_file(name, opts)
    sys.stdout.write("Syntaxes: %d\n" % len(SYNTAXES))
    sys.stdout.write("Encodings: %d\n" % len(ENCODINGS))
    
    dump(output)
    
    
if __name__ == '__main__':
    sys.exit(main())