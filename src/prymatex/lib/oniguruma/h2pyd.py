'''
Created on 23/11/2010

Converts .h definitions to Cython definitions

@author: defo
'''
import sys
import re

c_define_re = re.compile('''

    ^\#define\s             # The keyword
    (?P<name>[\w\_]+)\s+    # The constant name
    (?P<value>[\d]+)\s*$    # The numeric value
                 
''', re.VERBOSE)

def eval_line(line):
    '''
    Takes a text line and analyzes its contents
    '''
    match = c_define_re.match(line)
    if match:
        return "%s = %s" % (match.group('name'), match.group('value')) 

def handle_file(fp, dest = sys.stdout):
    '''
    @param fp: A file stream to read from
    @param dest: A file stream to write on, defaults to stdout.
    @return: Amount of times a python definition could be retrived
    '''
    counter = 0
    for line in fp.readlines():
        results = eval_line(line)
        if results:
            dest.write('%s\n' % results)
            counter += 1
    return counter

def main(argv = sys.argv):
    files = argv[1:]
    if not files:
        handle_file(sys.stdin)
    else:
        for fname in files:
            fp = open(fname)
            handle_file(fp)
            fp.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())