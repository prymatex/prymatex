#!/usr/bin/env python
# coding: utf-8

'''
Created on 23/11/2010

Converts .h definitions to Cython pxd definitions.
Diclaimer: It's highly oriented to oniguruma way of doing things.

@see http://docs.cython.org/src/tutorial/pxd_files.html

@author: defo
'''
import sys
import re
from optparse import OptionParser
from os.path import exists
import operator
# Some exceptions
class ConfigException(Exception):
    pass

class ArgumentException(ConfigException):
    pass


def largest_word(iterable):
    max_length = 0
    for word in iterable:
        cur_len = len(word) 
        if cur_len > max_length: cur_len
    return max_length

## {{{ http://code.activestate.com/recipes/52549/ (r3)
class curry:
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.pending = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs

        return self.fun(*(self.pending + args), **kw)
## end of http://code.activestate.com/recipes/52549/ }}}

class hash(dict):
    ''' Javascript-like object '''
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

def wrap_in_comment(line_or_lines):
    '''
    Wraps a string in comments plus some fancy heading
    '''
    lines = line_or_lines.split('\n')
    max_len = max(map(len, lines))
    size = max_len + 2
    line = '# %s\n' % ('-' * size, )
    line_block = [ "# %s\n" % l for l in lines ]
    return "%(line)s%(text)s%(line)s" % { 'line' : line,
    'text': ''.join(line_block)}

    

from datetime import datetime


HEADING = wrap_in_comment('''
This file was automatically generated, please do not edit.
Any modifications will be lost after a new h2cython call
Generated on %s''' % (datetime.now().strftime("%x at %X")))


                                           

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
    
    Allows to define regular expressions to be taken away from the resulting
    names as many C libraries prepend their name due to lack of namespaces,
    i.e.:
        #define MYLIBNAME_VALUE_A 1
        #define MYLIBNAME_VALUE_B 2
        
    
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
    
    # Loaded form the values dict passed in the __init__ method
    remove_from_name_regexes = []
    
    
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
        
        try:
            for reg in config.remove_exprs:
                self.remove_from_name_regexes.append(re.compile(reg))
        except Exception, e:
            raise ArgumentException("Bad regex %s" % e)
        
        self.values = {} # Values
        self.order = [] # Name - Value sociation, celan data
        self.pending_keys = [] # Values that could not yet be processed
        self.pending_dict = {} # The values
        
        self._match_collectors = {}
        
        self.add_match_collector('encoding',
                               re.compile('''
                               \#define\s+ONIG_(?P<name>ENCODING_[_\w\d]+)\s+\(\&[\d\w]+\)
                               ''', re.VERBOSE)) 
    
    
    def add_match_collector(self, name, regex):
        '''
        @param name: The name of the enumeration
        @param regex: A regex to detect these enum in lines
        @param initial: Initial value
        @param inc_fx: A callable with 2 arguments, the current value, ant the\
                       the match. Should return the next value.
                       By default it's a operator.add
        '''
        
            
        if name in self._match_collectors:
            raise ConfigException("Duplicate name")
        
        self._match_collectors[name] = hash(
                                      regex = regex,
                                      collected = [] ,
                                      )
    
    def parse(self):
        '''
        Parses the file
        '''
        for number, line in enumerate(self.file.readlines()):
            self.process_line(line)
            
            
    def search_constant_definition(self, line):
        match = self.regex.match( line.strip('\n') )
        if not match:
            return
        name = match.group('name')
        raw_value = match.group('value')
        comment = match.group('comment')
        clean_value = self.clean_value(raw_value)
         
        if self.is_valid_constant(clean_value):
            self[name] = clean_value
            
    def search_enumeration(self, line):
        for _name, config in self._match_collectors.iteritems():
            match = config.regex.match(line)
            if match:
                config.collected.append(match.group('name'))
    
    def process_line(self, line):
        
        if not self.search_constant_definition(line):
            # To 
            self.search_enumeration(line)
        
    
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
    
    def get_undefined_variable(self, exc_msg):
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
            
    
    
    
    def as_pxd(self, output = None, heading = HEADING):
        '''
        Writes to output the resulting pxd file
        @param output: A file like object
        @param heading: A heading to prepend to the text output
        '''
        
        if not output:
            output = self.output
        
        output.write(HEADING)
        
        
        width = largest_word(self.order) + 1
        format = "%-" + str(width) + "s = %s\n"
            
        for name, value in self.iter_clean():
            output.write(format % (name, value))
        
        for name, data in self._match_collectors.iteritems():
            if not data.collected:
                sys.stderr.write("No definitions for %s\n" % name)
                continue
            
            heading = wrap_in_comment("Definitions for %s" % name)
            output.write(heading)
            
            for n, element in enumerate(data.collected):
                output.write("%s = %d\n" % (element, n))
            #sys.stderr.write("n = %d" % n)
            
    
    def iter_clean(self):
        '''
        Generator that produces clean name, clean value tuples
        '''
        for name in self.order:
            yield (self.clean_name(name), self[name])
    
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

    def clean_name(self, name):
        for regex in self.remove_from_name_regexes:
            name = regex.sub('', name)
        return name

def handle_file(fp, cfg, output = sys.stdout):
    '''
    @param fp: A file stream to read from
    @param dest: A file stream to write on, defaults to stdout.
    @return: Amount of times a python definition could be retrived
    '''
    try:
        parser = HeaderFileParser(fp, config = cfg)
    except ArgumentException, e:
        sys.stderr.write("%s\n" % e)
        sys.exit(-3)
        
    parser.parse()
    parser.as_pxd(output)
    if cfg.verbose and not parser.is_clean():
        converted = len(parser.order)
        rejected = len(parser.pending_keys)
        total = converted + rejected
        conv_stat = float(rejected) / converted 
        sys.stderr.write("-"*50+"\n")
        sys.stderr.write("Definitions which could not be decoded were")
        sys.stderr.write(" (%d from %d %2.2f%%)\n" % (rejected, total, 
                                                    conv_stat))
        for name, value in parser.iter_pending():
            sys.stderr.write(" * %s = %s\n" % (name, value))
    
    
    
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
    
    parser.add_option('-r', '--remove-expr', dest = "remove_exprs", 
                      action = "append",
                      help = "Defines regular expressions to be removed"
                        "from the keys")
    parser.set_default("remove_exprs", [])
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