#!/usr/bin/env python
from xmlrpclib import ServerProxy
import sys
from optparse import OptionParser
# sum(map(lambda c: ord(c), 'Prymatex is an open source textmate replacement'))

PORT = 4612



def show_tooltip(args):
    '''
    tm_dialog tooltip --transparent --text|--html CONTENT
    '''
    parser = OptionParser()
    parser.add_option('--transparent', action = 'store_true', default = False,
                      help = 'Transparent tooltip')
    parser.add_option('--text', action = 'store_true', default = False,
                      help = 'Text', dest = 'format')
    parser.add_option('--html', action = 'store_true', default = False,
                      help = 'HTML', dest = 'format')
    options, content = parser.parse_args(args)
    #import ipdb; ipdb.set_trace()
    
    server = ServerProxy('http://localhost:%d' % PORT)
    retval = server.show_tooltip(options.transparent, 
                        options.format,
                        content)
    return retval

def print_help():
    print "?"

def main(argv = sys.argv[1:]):
    command = argv[0]
    if command == 'tooltip':
        return show_tooltip(argv[1:])
    else:
        print_help()
    
    

if __name__ == '__main__':
    main()
