#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import plistlib
import glob

PREFERENCES_PATH = os.environ['PMX_PREFERENCES_PATH'] if 'PMX_PREFERENCES_PATH' in os.environ else os.path.join(os.environ['HOME'], 'Library', 'Preferences')

def read(domain = None, key = None):
    '''
        read            Prints all of the user's defaults, for every domain, to standard output.
        read domain     Prints all of the user's defaults for domain to standard output.
        read domain key Prints the value for the default of domain identified by key.
    '''
    if domain == None:
        for domain in glob.glob(os.path.join(PREFERENCES_PATH, '*.plist')):
            read(domain)
    elif key == None:
        domain = domain if domain.endswith('.plist') else domain + '.plist'
        file = os.path.join(PREFERENCES_PATH, domain)
        if os.path.exists(file):
            print(plistlib.readPlist(file))
    else:
        domain = domain if domain.endswith('.plist') else domain + '.plist'
        file = os.path.join(PREFERENCES_PATH, domain)
        if os.path.exists(file):
            plist = plistlib.readPlist(file)
            if key in plist:
                print(plist[key])

def read_type():
    '''
        read-type domain key   Prints the plist type for the given domain identified by key.
    '''
    pass
    
def write(domain, key, value = None):
    '''
        write domain key 'value'
            Writes value as the value for key in domain.  value must be a property list, and must be
            enclosed in single quotes.  For example:

                defaults write com.companyname.appname "Default Color" '(255, 0, 0)'

            sets the value for Default Color to an array containing the strings 255, 0, 0 (the red,
            green, and blue components). Note that the key is enclosed in quotation marks because it
            contains a space.

        write domain 'plist'
            Overwrites the defaults information in domain with that given as plist.  plist must be a
            property list representation of a dictionary, and must be enclosed in single quotes.  For
            example:

                defaults write com.companyname.appname '{ "Default Color" = (255, 0, 0);
                                                "Default Font" = Helvetica; }';

            erases any previous defaults for com.companyname.appname and writes the values for the two
            names into the defaults system.
    '''
    if value == None and key[0] == "'" and key[-1] == "'":
        # the key is a plist
        pass
    else:
        domain = domain if domain.endswith('.plist') else domain + '.plist'
        file = os.path.join(PREFERENCES_PATH, domain)
        if os.path.exists(file):
            plist = plistlib.readPlist(file)
        else:
            plist = {}
        plist[key] = value
        plistlib.writePlist(plist, file)

def delete():
    '''
        delete domain      Removes all default information for domain.
        delete domain key  Removes the default named key from domain.
    '''
    pass
    
def domains():
    '''
        domains     Prints the names of all domains in the user's defaults system.
    '''
    pass

def find():
    '''
        find word   Searches for word in the domain names, keys, and values of the user's defaults, and prints out a list of matches.
    '''
    pass

def help():
    '''
        help        Prints a list of possible command formats.
    '''
    pass

# TODO Usar a argparse y migrar a pmxctl.py
def main(command, *args):
    if command == 'read':
        read(*args)
    elif command == 'read-type':
        read_type()
    elif command == 'write':
        write(*args)
    elif command == 'delete':
        delete()
    elif command == 'domains':
        domains()
    elif command == 'find':
        find()
    elif command == 'help':
        help()
    return 0

def ensure_preferences_path():
    if not os.path.exists(PREFERENCES_PATH):
        os.makedirs(PREFERENCES_PATH)
        
if __name__ == '__main__':
    ensure_preferences_path()
    sys.exit(main(*sys.argv[1:]))