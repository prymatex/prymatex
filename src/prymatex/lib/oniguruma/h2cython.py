#!/usr/bin/env python
# coding: utf-8

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

     
# Sotre values
CACHE = {}
REJECTED = []


def largest_word(iterable):
    max_length = 0
    for word in iterable:
        cur_len = len(word) 
        if cur_len > max_length: cur_len
    return max_length


class HeaderFileParser(object):
    '''
    Process a C header file looking for C constant definitions,
    i.e. 
        #define VALUE 1
    
    It also can handle some constants where they must be looked back in the
    file, i.e.:
        #define DEVAULT_VALUE VALUE_NONE
        
        #define VALUE_NONE 0
        
    In some cases C haders files contain bitwise operations where integers must
    be treated as unsigned, this is correctly hanlded, as wel as bit rotations,
    i.e.:
        #define VALUE 1U
        #define VALUE_A (VALUE << 1)
    
    '''
    # C #define regex
    regex = re.compile('''

        ^\#define\s                                 # The keyword
        (?P<name>[\w\_]+)\s+                        # The constant name
        (?P<value>[\-\d\w\_\>\<\U\(\\s)]+)          # The numeric value
        \s*(?P<comment>\/\*[\s\w\W\(\)]+\*\/)?$     # Comment's
                 
    ''', re.VERBOSE)
    
    name_exc_regex = re.compile('''
       name\s
       ["'](?P<name>.+)["']
       \sis\snot\sdefined                                                  
    ''', re.VERBOSE )
    
    # Handle integers with traling U's
    unsigned_int_regex = re.compile('''
        (?<=\d)U
    ''', re.VERBOSE)
    
    
    def __init__(self, file_or_name, config, output = sys.stdout):
        '''
        @param file_or_name: File or name
        @param output: Stream to write to
        '''
        if isinstance(file_or_name, basestring):
            self.file = open(file_or_name)
        else:
            self.file = file_or_name
        self.output = output
        self.rejected = []
        
        
        self.values = {} # Values
        self.order = [] # Name - Value sociation, celan data
        self.pending_keys = [] # Values that could not yet be processed
        self.pending_dict = {} # The values 
        
    def parse(self):
        for number, line in enumerate(self.file.readlines()):
            self.process_line(line)
            
            
    
    def process_line(self, line):
        match = self.regex.match( line.strip('\n') )
        if not match:
            return
        name = match.group('name')
        raw_value = match.group('value')
        comment = match.group('comment')
        
        
#        if name == "ONIG_OPTION_NONE":
#            from ipdb import set_trace; set_trace()
            
        clean_value = self.clean_value(raw_value)
         
        if self.is_valid_constant(clean_value):
            self[name] = clean_value
    
    def clean_value(self, value):
        '''
        Cleans some integer definitions.
        '''
        return self.unsigned_int_regex.sub('', value)    
        
    def __getitem__(self, name):
        return self.values.__getitem__(name)
    
    def __setitem__(self, name, value):
        try:
            final_value = eval(value, self.values)
            
        except NameError, e:
            #from ipdb import set_trace; set_trace()
            # Keep the dictoinary for evals clean
            self.pending_keys.append(name)
            self.pending_dict[name] = value
            #from ipdb import set_trace; set_trace()
        
        except SyntaxError, e:
            # Some stuff C has, python cant eval
            pass
        
        else:   
            self.order.append(name)
            self.values[name] = final_value 
    
    def get_undefined_name(self, exc_msg):
        '''
        Parses a NameError exception string. This method relies on Python
        exception messages.
        
        
        @returns The name of the undefined reference
        '''
        match = self.name_exc_regex.search(str(exc_msg))
        if match:
            return match.group('name')
    
    def is_valid_constant(self, name):
        '''
        Checks if a constnt respects C uppercase convention.
        A constat like THIS_IS_MY_CONSTANT will pass the test while a
        constant defined as ThiCoolConstant will fail the test.
        This simple method greately simplifies type aliasing from constant
        definition.
        '''
        return name.upper() == name
    
    def itevalues(self):
        '''
        Iterates over values
        '''
        for name in self.order:
            yield name, self.values[name]
            
    
    def as_pxd(self, output = None):
        '''
        Writes to output the resulting pxd file
        '''
        if not output:
            output = self.output
            
        width = largest_word(self.order) + 1
        format = "%-" + str(width) + "s = %s\n"
            
        for name in self.order:
            output.write(format % (name, self[name]))
        
        
    
    def iter_pending(self):
        '''
        Returns values which could not be calculated
        '''
        for name in self.pending_keys:
            yield (name, self.pending_dict[name])
            
    def is_clean(self):
        '''
        '''
        return len(self.pending_keys) == 0
    
    def is_empty(self):
        return len(self.values) == 0



def handle_file(fp, cfg, output = sys.stdout):
    '''
    @param fp: A file stream to read from
    @param dest: A file stream to write on, defaults to stdout.
    @return: Amount of times a python definition could be retrived
    '''
    
    parser = HeaderFileParser(fp, config = cfg)
    parser.parse()
    parser.as_pxd(output)
    if cfg.verbose and not parser.is_clean():
        sys.stderr.write("-"*50+"\n")
        sys.stderr.write("Definitions that could not be decoded are:")
        sys.stderr.write(" (%d)\n" % len(parser.pending_keys))
        for name, value in parser.iter_pending():
            sys.stderr.write("%s = %s\n" % (name, value))
    
    
    
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
    
    parser.add_option("-v", "--verbose", default = False, action = "store_true",
                      help = "Be verbose")
    cfg, files = parser.parse_args(argv[1:])
    
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
        sys.stderr.write("Reading from stdin\n")
        sys.stderr.flush()
        try:
            handle_file(sys.stdin, output = output, cfg =  cfg )
        except KeyboardInterrupt:
            pass
    else:
        for fname in files:
            fp = open(fname)
            handle_file(fp, output = output, cfg = cfg )
            fp.close()
    if output != sys.stdout:
        output.close()
    #from pprint import pprint
    #pprint(CACHE)
    return 0

if __name__ == "__main__":
    sys.exit(main())