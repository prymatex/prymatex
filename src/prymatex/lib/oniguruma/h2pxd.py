#!/usr/bin/env python
'''
Created on 23/11/2010

Converts .h definitions to Cython definitions

@author: defo
'''
import sys
import re
from optparse import OptionParser

c_define_re = re.compile('''

    ^\#define\s                         # The keyword
    (?P<name>[\w\_]+)\s+                # The constant name
    (?P<value>\(?[\-\d\w\_\>\<\U]+\)?)        # The numeric value
    \s*(?P<comment>\/\*[\s\w\W\(\)]+\*\/)?$    # Comment's
                 
''', re.VERBOSE)

def process_value(name, value, cfg):
    '''
    
    '''
    return value.replace('U', '')




def eval_line(line, number, cfg):
    '''
    Takes a text line and analyzes its contents
    '''
    match = c_define_re.match(line)
    if match:
        name = match.group('name')
        value = process_value(name, match.group('value'), cfg)
        if match.group('comment'):
            comment = "# %s" % match.group('comment') 
        else:
            comment = '' 
        return "%s = %s %s" % (name, value, comment) 

def handle_file(fp, cfg, dest = sys.stdout):
    '''
    @param fp: A file stream to read from
    @param dest: A file stream to write on, defaults to stdout.
    @return: Amount of times a python definition could be retrived
    '''
    counter = 0
    for number, line in enumerate(fp.readlines()):
        results = eval_line(line, number = number, cfg = cfg)
        if results:
            dest.write('%s\n' % results)
            counter += 1
    return counter

def main(argv = sys.argv):
    '''
    Entry point, accepts a list of files or stdin
    '''
    #usage, option_list, option_class, version, conflict_handler, description, formatter, add_help_option, prog, epilog
    parser = OptionParser(description = "A simple regex conversor for C defs",
                          )
    parser.add_option('-o', '--ouput', help = "Output file (defaults to "
                      "stdout)", default = None)
    parser.add_option('-l', '--linenumbers', help = "Print line numbers in "
                      "comments", action = "store_true")
    parser.add_option("-c", "--comments", help = "Print comments")
    parser.add_option("-s", "--substitute", help = "Substitute values")
    
    cfg, args = parser.parse_args(argv)
    
    files = args[1:]
    if not files:
        handle_file(sys.stdin, cfg)
    else:
        for fname in files:
            fp = open(fname)
            handle_file(fp, cfg)
            fp.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())