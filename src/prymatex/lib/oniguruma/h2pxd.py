#!/usr/bin/env python
'''
Created on 23/11/2010

Converts .h definitions to Cython pxd definitions
@see http://docs.cython.org/src/tutorial/pxd_files.html

@author: defo
'''
import sys
import re
from optparse import OptionParser
from os.path import exists

c_define_re = re.compile('''

    ^\#define\s                         # The keyword
    (?P<name>[\w\_]+)\s+                # The constant name
    (?P<value>\(?[\-\d\w\_\>\<\U]+\)?)        # The numeric value
    \s*(?P<comment>\/\*[\s\w\W\(\)]+\*\/)?$    # Comment's
                 
''', re.VERBOSE)

# Sotre values
CACHE = {}

def process_value(name, value, cfg):
    '''
    Makes some adjustments to values
    '''
    global CACHE
    final_value = None
    
    value = value.replace('U', '') # Remove unsigned
    
    if value.upper() != value:
        return
    
    try:
        final_value = eval(value, CACHE) # Cache are globals
    except Exception, _e:
        #print e, name, value
        pass
    
    if not CACHE.has_key(value):
        CACHE[name] = final_value
         
    return final_value



def eval_line(line, number, cfg):
    '''
    Takes a text line and analyzes its contents
    '''
    match = c_define_re.match(line)
    if match:
        name = match.group('name')
        value = process_value(name, match.group('value'), cfg)
        
        if not value:
            # Value discarded, maybe it's not something you can translate
            # to python. 
            return
        
        if match.group('comment') and cfg.comments:
            comment = "# %s" % match.group('comment') 
        else:
            comment = ''
        if cfg.linenumbers:
            linenumber = '# From line %d\n' % number
        else:
            linenumber = ''
        
        return "%s%s = %s %s" % (linenumber, name, value, comment) 

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
    #usage, option_list, option_class, version, conflict_handler, description, 
    # formatter, add_help_option, prog, epilog
    parser = OptionParser(description = "A simple regex conversor for C defs",
                          )
    parser.add_option('-o', '--output', help = "Output file (defaults to "
                      "stdout)", default = None)
    parser.add_option('-f', '--force-overwrite', dest='overwrite',
                      default = False, action = "store_true",
                      help = "Overwrite output file if exists")
    parser.add_option('-l', '--linenumbers', help = "Print line numbers in "
                      "comments", action = "store_true", default = False)
    parser.add_option("-c", "--comments", help = "Include comments if"
                      "available")
    parser.add_option("-s", "--substitute", help = "Substitute values")
    parser.add_option("-i", "--include-original", dest="include",
                      action = "store_true", default = False)
    
    cfg, args = parser.parse_args(argv)
    
    files = args[1:]
    
    if cfg.output:
        if exists(cfg.output) and not cfg.overwrite:
            sys.stderr.write("%s already exists. Try --force-overwrite." % 
                             cfg.output)
            sys.exit(1)
        else:
            output = open(cfg.output, 'w')
    else:
        output = sys.stdout
        
    
    if not files:
        handle_file(sys.stdin, dest = output, cfg =  cfg)
    else:
        for fname in files:
            fp = open(fname)
            handle_file(fp, cfg = cfg, dest = output)
            fp.close()
    if output != sys.stdout:
        output.close()
    #from pprint import pprint
    #pprint(CACHE)
    return 0

if __name__ == "__main__":
    sys.exit(main())