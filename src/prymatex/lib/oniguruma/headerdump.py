'''
Created on 14/11/2010

@author: defo

Dump some files
'''
import sys
from optparse import OptionParser

def get_file():
    ''' Gets a file from your includes '''
    

def main(argv = sys.argv):
    '''
    Converts .h definitions which are not exported from 
    '''
    parser = OptionParser()
    
    opts, files = parser.parse_args(argv[1:])
    
    for name in files:
        get_header_file()
        
    

if __name__ == "__main__":
    sys.exit(main())
